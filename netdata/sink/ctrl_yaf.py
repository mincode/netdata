#!/home/ec2-user/anaconda3/bin/python

import sys
import subprocess
import re


__author__ = 'Manfred Minimair <manfred@minimair.org>'


yaf_file = '/usr/local/etc/yaf.conf'
tmp_file = '/tmp/yaf.conf'

def_idle = 0
def_active = 60


def yaf_get():
    with open(yaf_file, 'r') as fin:
        for line in fin:
            if re.match('\W*YAF_EXTRAFLAGS', line):
                print(line)


def yaf_set(idle, active):
    flags = 'YAF_EXTRAFLAGS="--silk --applabel --idle-timeout={} --active-timeout={} --max-payload=2048 --plugin-name=/usr/local/lib/yaf/dpacketplugin.la"\n'
    with open(yaf_file, 'r') as fin:
        with open(tmp_file, 'w') as fout:
            for line in fin:
                if re.match('\W*YAF_EXTRAFLAGS', line):
                    # print(flags.format(idle, active))
                    fout.write(flags.format(idle, active))
                else:
                    fout.write(line)
    sudo = '/usr/bin/sudo'
    cmd = [sudo, 'cp', tmp_file, yaf_file]
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    print(res)
    cmd = [sudo, '/etc/init.d/yaf', 'restart']
    subprocess.run (cmd)


def yaf_restart():
    sudo = '/usr/bin/sudo'
    cmd = [sudo, '/etc/init.d/yaf', 'restart']
    subprocess.run (cmd)


def main():
    params = ('parameters: <restart|get|' +
              'reset [to {}, {}]|set idle-timeout active-timeout>'.
              format(def_idle, def_active))

    if len(sys.argv) < 2:
        print(params)
        quit()

    if sys.argv[1] == 'restart':
        yaf_restart()
    elif sys.argv[1] == 'get':
        yaf_get()
    elif sys.argv[1] == 'reset':
        yaf_set(def_idle, def_active)
    elif sys.argv[1] == 'set':
        if len(sys.argv) < 4:
            print(params)
            quit()
        else:
            idle = int(sys.argv[2])
            active = int(sys.argv[3])
            yaf_set(idle, active)
    else:
        print(params)
        quit()


if __name__ == '__main__':
    main()
