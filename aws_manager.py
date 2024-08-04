import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class AWSManager():
    REGION = 'us-east-2'
    KEY_NAME = 'MyAutoKeyPair'
    AMI_ID = 'ami-0264c259d0b94760e'
    INSTANCE_TYPE = 't2.large'
    REGION = 'us-east-2'
    SECURITY_GROUP_NAME = 'file_test_handler'
    SECURITY_GROUP_DESCRIPTION = 'Security group designed for file handling'

    def __init__(self, key_path):
        '''Constructor.'''
        self.ec2 = None
        self.ec2_client = None
        self.security_group_id = None
        self.host_ip = None
        self.instances = []
        self.key_path = os.path.join(key_path, self.KEY_NAME + '.pem')
        try:
            self.set_up_client()
        except NoCredentialsError:
            print("Error: AWS credentials not found.")
        except PartialCredentialsError:
            print("Error: Incomplete AWS credentials.")
        except Exception as e:
            print(f"Unexpected error during AWS client setup: {e}")

    def set_up_client(self):
        '''Initialize AWS client.'''
        self.ec2 = boto3.resource('ec2', region_name=self.REGION)
        self.ec2_client = boto3.client('ec2', region_name=self.REGION)

    def key_pair_exists(self):
        '''Check if a key pair exists.'''
        try:
            self.ec2_client.describe_key_pairs(KeyNames=[self.KEY_NAME])
            return True
        except self.ec2_client.exceptions.ClientError as e:
            if 'InvalidKeyPair.NotFound' in str(e):
                return False
            raise

    def create_key_pair(self):
        '''Create a key pair.'''
        if not self.key_pair_exists():
            try:
                response = self.ec2_client.create_key_pair(KeyName=self.KEY_NAME)
                private_key = response['KeyMaterial']
                # Save the private key to a file
                with open(self.key_path, 'w') as key_file:
                    key_file.write(private_key)
                # Set permissions on the key file
                os.chmod(self.key_path, 0o400)
            except ClientError as e:
                print(f"Error creating key pair: {e}")
                raise
            except IOError as e:
                print(f"Error writing key file: {e}")
                raise

    def security_group_exists(self):
        '''Check if a security group exists.'''
        try:
            response = self.ec2_client.describe_security_groups(
                Filters=[{'Name': 'group-name', 'Values': [self.SECURITY_GROUP_NAME]}]
            )
            if response['SecurityGroups']:
                return response['SecurityGroups'][0]['GroupId']
            return False
        except ClientError as e:
            print(f"Error checking security group existence: {e}")
            raise

    def create_security_group(self):
        '''Create a security group.'''
        if not self.security_group_exists():
            try:
                response = self.ec2_client.create_security_group(
                    GroupName=self.SECURITY_GROUP_NAME,
                    Description=self.SECURITY_GROUP_DESCRIPTION
                )
                self.security_group_id = response['GroupId']

                self.ec2_client.authorize_security_group_ingress(
                    GroupId=self.security_group_id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )
            except ClientError as e:
                print(f"Error creating security group: {e}")
                raise

    def launch_instances(self, user_data='', number_instances=3):
        '''Create an EC2 instance.'''
        self.instances = self.ec2.create_instances(
                ImageId=self.AMI_ID,
                MinCount=number_instances,
                MaxCount=number_instances,
                InstanceType=self.INSTANCE_TYPE,
                KeyName=self.KEY_NAME,
                SecurityGroups=[self.SECURITY_GROUP_NAME],
                UserData=user_data
                )
        self.wait_for_instances()
    
    def stop_instances(self):
        '''Stop EC2 instances.'''
        instance_ids = [instance.id for instance in self.instances]
        self.ec2_client.terminate_instances(InstanceIds=instance_ids)

    def get_orchestrator_host_ip(self):
        '''Get orchestrator host ip.'''
        response = self.ec2_client.describe_instances(
            Filters=[{'Name': 'tag:Name', 'Values': ['orchestrator']}]
        )
        self.host_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    def wait_for_instances(self):
        '''Wait for instances to start running.'''
        for instance in self.instances:
            instance.wait_until_running()
        for instance in self.instances:
            instance.reload()

    def get_host_ip(self):
        '''Getter for host ip.'''
        return self.host_ip

    def get_instances(self):
        '''Getter for created instances.'''
        return self.instances
    
    def get_security_group_id(self):
        '''Getter for security group id.'''
        return self.security_group_id

    def get_key_path(self):
        '''Getter for key path.'''
        return self.key_path
