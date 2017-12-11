#!/home/ec2-user/anaconda3/bin/python

import sys
from paramiko.client import SSHClient, AutoAddPolicy

from ami_manager import AmiManager
from defaults import sink_instance


__author__ = 'Manfred Minimair <manfred@minimair.org>'


def_idle = 1
def_active = 60
ctrl_yaf = '/home/ec2-user/gitProjects/netdata/netdata/sink/ctrl_yaf.py'


def start_client():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    return client


def main():
    params = ('parameters: < restart | get |' +
              'set idle-timeout active-timeout | reset [to {}, {}] >'.
              format(def_idle, def_active))

    if len(sys.argv) < 2:
        print(params)
        quit()

    client = start_client()
    a = AmiManager(sink_instance)

    if sys.argv[1] == 'restart':
        cmd = ctrl_yaf + ' ' + 'restart'
        status = a.exec_all(client, cmd)
    elif sys.argv[1] == 'get':
        cmd = ctrl_yaf + ' ' + 'get'
        status = a.exec_all_print(client, cmd)
    elif sys.argv[1] == 'reset':
        cmd = ctrl_yaf + ' ' + 'reset'
        status = a.exec_all(client, cmd)
    elif sys.argv[1] == 'set':
        if len(sys.argv) < 4:
            print(params)
            quit()
        else:
            idle = int(sys.argv[2])
            active = int(sys.argv[3])
            cmd = ctrl_yaf + ' ' + 'set {} {}'.format(idle, active)
            status = a.exec_all(client, cmd)
    else:
        print(params)
        quit()
    
    if status:
        print(status)


if __name__ == '__main__':
    main()
