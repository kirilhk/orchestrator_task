import pathlib
import getpass
import argparse
from aws_manager import AWSManager
from payload_manager import PayloadManager
from statistics_handler import StatisticsManager


class Orchestrator():
    SCRIPT_PATH = '/home/ubuntu/payload.py'
    ORCHESTRATOR_USER = getpass.getuser()


    def __init__(self, log_type):
        '''Constructor.'''
        self.log_type = log_type
        self.instances = []
        self.payload_instances = []
        self.key_path = ''
        self.aws_manager_instance = None
        self.statistics_instance = None

# This is the POC for when the script is executed on boot and syncs the files back to host

    # def run(self):
    #     '''Run function.'''
    #     try:
    #         self.set_up_infrastructure()
    #         self.wait_for_stats()
    #     except:
    #         print('Failed to gather statistics.')
    #         raise

    # def set_up_infrastructure(self):
    #     '''Set up whole AWS infra needed for VM creation'''
    #     self.aws_manager_instance = AWSManager(self.key_path)
    #     self.aws_manager_instance.create_key_pair()
    #     self.aws_manager_instance.create_security_group()
    #     self.aws_manager_instance.get_orchestrator_host_ip()
    #     self.key_path = self.aws_manager_instance.get_key_path()
    #     host_ip = self.aws_manager_instance.get_host_ip()
    #     user_data = PayloadManager.collect_cloud_init_script(host_ip, 'ubuntu', self.key_path)
    #     self.aws_manager_instance.launch_instances(user_data=user_data,
    #                                                number_instances=1)

    # def wait_for_stats(self):
    #     '''Wait for statistics.'''
    #     StatisticsManager.create_statistics_dir()
    #     self.statistics_instance = StatisticsManager(self.log_type)
    #     self.statistics_instance.wait_for_statistics()
    #     self.statistics_instance.load_statistics()
    #     self.statistics_instance.print_statistics()

# This is POC for when the VMs do not execute the script on boot but 
# instead the orchestrator starts them manualy and waits for them 

    # def run(self):
    #     '''Run functions.'''
    #     try:
    #         self.set_up_infrastructure()
    #         self.distribute_payload()
    #         self.collect_statistics()
    #     except:
    #         self.clean_up()
    #         raise
    #     self.clean_up()

    # def set_up_infrastructure(self):
    #     '''Set up the whole AWS infra needed for VM creation.'''
    #     self.aws_manager_instance = AWSManager(self.key_path)
    #     self.aws_manager_instance.create_key_pair()
    #     self.aws_manager_instance.create_security_group()
    #     self.aws_manager_instance.launch_instances(1)
    #     self.instances = self.aws_manager_instance.get_instances()
    #     self.key_path = self.aws_manager_instance.get_key_path()
    #     print(self.key_path)
    
    # def distribute_payload(self):
    #     '''Distributes the payload script to the VMs.'''
    #     for instance in self.instances:
    #         payload_instance = PayloadManager(instance, self.key_path)
    #         payload_instance.distribute_script('payload.py', self.SCRIPT_PATH)
    #         payload_instance.run_script(f'python3 {self.SCRIPT_PATH}')
    #         self.payload_instances.append(payload_instance)

    #     # Wait for the instances to finish the payload script
    #     for p_instance in self.payload_instances:
    #         p_instance.check_if_finished()

    # def collect_statistics(self):
    #     '''Collect statistics about the VMs.'''
    #     self.statistics_instance = StatisticsManager(self.instances, self.key_path, self.log_type)
    #     self.statistics_instance.gather_all_statistics()
    #     self.statistics_instance.print_statistics()

    # def clean_up(self):
    #     '''Clean up.'''
    #     self.aws_manager_instance.stop_instances()
    #     for p_instance in self.payload_instances:
    #         p_instance.remove_done_file()


def parse_arguments():
    '''Argument parser.'''
    parser = argparse.ArgumentParser(description='Select logging type: human-readable or JSON.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-hr', '--human-readable', action='store_true', help='Enable human readable logging')
    group.add_argument('-j', '--json', action='store_true', help='Enable JSON logging')

    return parser.parse_args()

def get_logging_type(args):
    '''Parse the input.'''
    if args.human_readable:
        return 'human-readable'
    elif args.json:
        return 'json'
    else:
        raise ValueError('Invalid logging type selected.')


def main():
    '''Main function.'''
    args = parse_arguments()
    logging_type = get_logging_type(args)
    orchestrator = Orchestrator(logging_type)
    orchestrator.run()


if __name__ == '__main__':
    main()

