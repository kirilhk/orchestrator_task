import paramiko


class SSHManager():

    def __init__(self, instance_dns, key_path):
        '''Constructor.'''
        self.instance_dns = instance_dns
        print(instance_dns)
        self.key_path = key_path
        self.ssh = None

    def setup_ssh_client(self):
        '''Create SSH client.'''
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.instance_dns, username='ubuntu', key_filename=self.key_path)

    def execute_command(self, command):
        '''Execute remote command via SSH client.'''
        self.setup_ssh_client()
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdin,stdout, stderr

    def send_file(self, file_location, file_destination):
        '''Send file via sftp.'''
        self.setup_ssh_client()
        sftp = self.ssh.open_sftp()
        sftp.put(file_location, file_destination)
        sftp.close()
        self.ssh.close()

    def get_file(self, file_location, file_destination):
        '''Get a file via sftp.'''
        self.setup_ssh_client()
        sftp = self.ssh.open_sftp()
        sftp.get(file_location, file_destination)
        sftp.close()
        self.ssh.close()
