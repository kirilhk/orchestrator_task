import os
import json
import time
from SSH_manager import SSHManager


class StatisticsManager():

    def __init__(self,log_type, instances=None, key_path=None):
        '''Constructor.'''
        self.instances = instances
        self.key_path = key_path
        self.log_type = log_type
        self.all_stats = {}

    def gather_statistics(self, instance='',statistics_path='/home/ubuntu/stats.json'):
        '''Gather statistics for a single instance.'''
        stats = {}
        ssh_instance = SSHManager(instance.public_dns_name, self.key_path)
        ssh_instance.get_file(statistics_path, f'stats_{instance.id}.json')

        with open(f'stats_{instance.id}.json', 'r') as stats_file:
            stats = json.load(stats_file)
        return stats

    def gather_all_statistics(self):
        '''Gather statistics for all instances given.'''
        for instance in self.instances:
            self.all_stats[instance.id] = self.gather_statistics(instance)

    def print_statistics(self):
        '''Print statistics based on user input.'''
        if self.log_type == 'json':
            print(json.dumps(self.all_stats, indent=4))
        else:
            for key, value in self.all_stats.items():
                print(f'For VM instance {key}, Creation time was:{value['create_time']}, Copy time was: {value['copy_time']}, Deletion was: {value['delete_time']}')
    
    @staticmethod
    def create_statistics_dir(folder_path='/home/ubuntu/statistics'):
        '''Create statistics directory.'''
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def wait_for_statistics(self, folder_path='/home/ubuntu/statistics'):
        '''Wait for the VMs to finish execution.'''
        iterations = 0
        while True or iterations < 20:
            files = os.listdir(folder_path)
            if files and len(files) % 3 == 0:
                break
            time.sleep(2)
            iterations += 1
        if iterations == 20:
            raise Exception('Failed to gather all the statistics.')

    def load_statistics(self, folder_path='/home/ubuntu/statistics'):
        '''Load the statistics.'''
        files = os.listdir(folder_path)
        for file in files:
            if os.path.exists:
                with open(os.path.join(folder_path, file), 'r') as f:
                    self.all_stats[file] = json.load(f)
        