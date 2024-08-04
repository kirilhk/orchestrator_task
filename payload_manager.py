import time
from SSH_manager import SSHManager


class PayloadManager():
    CHECK_INTERVAL = 25
    HOME_PATH = '/home/ubuntu/'
    CLOUD_INIT_TEMPLATE_PATH = 'cloud_init.txt'

    def __init__(self, instance, key_path):
        '''Constructor.'''
        self.instance = instance
        self.key_path = key_path
        self.ssh_instance = SSHManager(self.instance.public_dns_name, key_path)

    def distribute_script(self, script_location, remote_location):
        '''Distribute the payload script.'''
        self.ssh_instance.send_file(script_location, remote_location)

    def run_script(self, command):
        '''Run the payload script.'''
        return self.ssh_instance.execute_command(command)

    def check_if_finished(self):
        '''Waits for the process to finish.'''
        iters = 0
        while True or iters < 40:
            stdin, stdout, stderr = self.run_script(f"test -f {self.HOME_PATH}destination/done && echo 'DONE'")
            if stdout.read().decode().strip() == 'DONE':
                break
            time.sleep(self.CHECK_INTERVAL)
            iters += 1

    def remove_done_file(self):
        '''Remove done file.'''
        self.run_script('rm -rf /home/ubuntu/destination/done')

    @staticmethod
    def collect_cloud_init_script(orchestrator_host, orchestrator_user, key_path):
        '''Modify cloud script based on the orchestrator host and ip.'''
        with open(PayloadManager.CLOUD_INIT_TEMPLATE_PATH, 'r') as file:
            cloud_init_script = file.read()
        cloud_init_script = PayloadManager.modify_cloud_init_script(cloud_init_script,
                                                                    orchestrator_host,
                                                                    orchestrator_user,
                                                                    key_path)
        return cloud_init_script
    
    @staticmethod
    def parse_key_pair(key_pair):
        '''Add spacing to key pair to fit cloud init.'''
        parsed_key_pair = []
        for line in key_pair:
            temp_line = f'      {line}'
            parsed_key_pair.append(temp_line)
        return ''.join(parsed_key_pair)

    @staticmethod
    def get_key_pair(key_path):
        '''Return parsed key pair.'''
        try:
            with open(key_path, 'r') as f:
                key_lines = f.readlines()
            key_pair = PayloadManager.parse_key_pair(key_lines)
            return key_pair
        except:
            print('Failed to get key pair')
            raise

    @staticmethod
    def modify_cloud_init_script(cloud_init_script ,orchestrator_host, orchestrator_user, key_path):
        cloud_init_script = cloud_init_script.replace('<orchestrator_host>',
                                                      orchestrator_host)
        cloud_init_script = cloud_init_script.replace('<orchestrator_user>',
                                                      orchestrator_user)
        cloud_init_script = cloud_init_script.replace('<key_value>',PayloadManager.get_key_pair(key_path))
        return cloud_init_script