import os
import boto3
from botocore.exceptions import ClientError
from netdata.workers.worker_table import WorkerTable
from netdata.workers.paths import get_home_dir


class AmiManager:
    cfg = None  # dict of instance config data; see defaults.py
    workers = None  # WorkerTable
    ec2 = None  # boto3 resource ec2

    def __init__(self, instance_cfg, path=''):
        """
        Init.
        :param instance_cfg: dict of instance data; see defaults.py
        :param path: path to store instance info; default is home dir
        """
        self.cfg = instance_cfg
        self.ec2 = boto3.resource('ec2')
        target_dir = path if path else get_home_dir()
        save_dir = os.path.join(target_dir, self.cfg['table_dir'])
        self.workers = WorkerTable(
            save_dir,
            self.cfg['storage'], 
            self.cfg['first_ip'])

    @property
    def workers_count(self):
        """
        Count all workers.
        :return: coutn of all workers.
        """
        return len(self.workers.all_ids)

    def start_all(self):
        self.ec2.instances.start(InstanceIds=self.workers.all_ids)

    def stop_all(self):
        self.ec2.instances.stop(InstanceIds=self.workers.all_ids)

    def terminate_all(self):
        self.ec2.instances.terminate(InstanceIds=self.workers.all_ids)
        self.workers.delete_all()

    def exec_all(self, ssh_client, cmd):
        """
        Execute remote command on all clients.
        :param ssh_client: paramiko.client.SSHClient
        :param cmd: command string
        :return: list of pairs (ip, exit status of cmd)
        """
        status = list()
        for ip in self.workers.all_ips:
            ssh_client.connect(ip)
            print('ami: ' + ip)
            print('cmd: ' + cmd)
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            status.append((ip, exit_status))
        return status

    def exec_all_print(self, ssh_client, cmd):
        """
        Execute remote command on all clients and print stdout of command.
        :param ssh_client: paramiko.client.SSHClient
        :param cmd: command string
        :return: list of pairs (ip, exit status of cmd)
        """
        status = list()
        for ip in self.workers.all_ips:
            ssh_client.connect(ip)
            print('ami: ' + ip)
            print('cmd: ' + cmd)
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            for line in stdout.readlines():
                print(line.rstrip('\n'))
            status.append((ip, exit_status))
        return status

    def launch(self, count=1):
        """ 
        Launch workers from ami.
        :param count: number of workers.
        """
        for i in range(count):
            index = self.workers.next_index
            ip = self.workers.next_ip(index)
            try:
                res = self.ec2.create_instances(
                    ImageId=self.cfg['ami'],
                    SecurityGroupIds=self.cfg['security'], 
                    SubnetId=self.cfg['net_subnet'], 
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=self.cfg['instance_type'],
                    KeyName=self.cfg['key_name'],
                    PrivateIpAddress=ip,
                    #DryRun = True,
                )
                print(res)
                #class anonym:
                #    id = 0
                #    def __init__(self, count):
                #        self.id = str(count)
                #res = [anonym(count)]
                self.workers.insert(index, ip, res[0].id)
            except ClientError as e:
                print(e)
                #if 'DryRunOperation' not in str(e):
                #    raise
