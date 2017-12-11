#!/home/ec2-user/anaconda3/bin/python

import sys
from ami_manager import AmiManager
from defaults import sink_instance, sender_instance


def main():
    params = 'parameters: <sinks|senders> \
<launch num|terminate|start|stop|count>'

    if len(sys.argv) < 3:
        print(params)
        quit()

    if sys.argv[1] == 'sinks':
        a = AmiManager(sink_instance)
    elif sys.argv[1] == 'senders':
        a = AmiManager(sender_instance)
    else:
        print(params)
        quit()

    if sys.argv[2] == 'launch':
        if len(sys.argv) < 4:
            print(params)
            quit()
        else:
            count = int(sys.argv[3])
            a.launch(count)
    elif sys.argv[2] == 'terminate':
        a.terminate_all()
    elif sys.argv[2] == 'start':
        a.start_all()
    elif sys.argv[2] == 'stop':
        a.stop_all()
    elif sys.argv[2] == 'count':
        print('{} count: {}'.format(sys.argv[1], a.workers_count))
    else:
        print(params)
        quit()


if __name__ == '__main__':
    main()
