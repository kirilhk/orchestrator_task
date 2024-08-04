import os
import time
from datetime import datetime
import json
import shutil
import subprocess

# def foo(folder_path, num_files, action):
#     try:
#         start_time = time.time()
#         getattr(action,)
#         end_time = time.time()
#     except:
#         ...
    
#     return end_time - start_time

ORCHESTRATOR_HOST = '<orchestrator_host>'
ORCHESTRATOR_USER = '<orchestrator_user>'
ORCHESTRATOR_KEY_PATH = '/home/ubuntu/orchestrator_key.pem'




def create_files(folder_path, num_files):
    '''Create files.'''
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    start_time = time.time()
    for i in range(num_files):
        file_path = os.path.join(folder_path, f'file_{i}.txt')
        with open(file_path, 'w') as f:
            f.write('Test')

    end_time = time.time()
    return end_time - start_time

def copy_files(src_folder, dst_folder):
    '''Copy files from src to dst.'''
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    start_time = time.time()
    for file_name in os.listdir(src_folder):
        src_file_path = os.path.join(src_folder, file_name)
        dst_file_path = os.path.join(dst_folder, file_name)
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dst_file_path)
    end_time = time.time()
    return end_time - start_time

def delete_files(folder_path):
    '''Delete files from src and dst.'''
    start_time = time.time()
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    end_time = time.time()
    return end_time - start_time

def transfer_back_statistics():
    '''Transfers the statistics back.'''
    nanoseconds = time.time_ns() % 1_000_000_000
    timestamp = datetime.now.strftime('%Y%m%d_%H%M%S')
    file_extension = f'{timestamp}_{nanoseconds:09d}'
    subprocess.run([
        'scp',
        '-i', ORCHESTRATOR_KEY_PATH,
        f'{home_path}/stats.json',
        f'{ORCHESTRATOR_USER}@{ORCHESTRATOR_HOST}:/home/{ORCHESTRATOR_USER}/statistics/stats_{file_extension}.json'
    ])


if __name__ == '__main__':
    home_path = '/home/ubuntu'
    folder_path = '/home/ubuntu/source'
    copy_folder_path = '/home/ubuntu/destination'
    num_files = 5

    create_time = create_files(folder_path, num_files)
    copy_time = copy_files(folder_path, copy_folder_path)
    delete_time = delete_files(folder_path)
    # delete_time += delete_files(copy_folder_path)

    stats = {
        'create_time': create_time,
        'copy_time': copy_time,
        'delete_time': delete_time
    }

    with open('/home/ubuntu/stats.json', 'w') as stats_file:
        json.dump(stats, stats_file)

    with open(f'{copy_folder_path}/done', 'w') as f:
        f.write('done')

    # transfer_back_statistics()