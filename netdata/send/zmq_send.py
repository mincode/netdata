#!/home/ec2-user/anaconda3/bin/python
# needs to be run with sudo for using port 80

import sys
import zmq

class TcpSender:
    """Send byte strings of fixed length.
    """
    def_msg = b'hey_ya'  # default message to send
    def_host = '127.0.0.1'  # default host
    def_port = 5005  # default port
    #def_port = 2323  # default control port

    context = None  # zmq context
    sink_socket = None  # a socket

    def __init__(self, sock=None):
        """
        Initialize as stream socket.
        :param sock: socket to use.
        """
        self.context = zmq.Context()
        self.sink_socket = self.context.socket(zmq.REQ)

    def connect(self, host=def_host, port=def_port):
        print('Connect to {0}:{1}'.format(host, port))
        self.sink_socket.connect('tcp://{0}:{1}'.format(host, port))

    def send(self, msg=def_msg):
        self.sink_socket.send(msg)
        print('expecting echo')
        data = self.sink_socket.recv()
        print("received data:", str(data, 'utf-8'))


import time

if len(sys.argv) <= 1:
    print('Parameters: <number of messages> [target ip] [message string]')
    print('Default message: {}'.format(TcpSender.def_msg))
    repeat = 0
else:
    repeat = int(sys.argv[1])

if len(sys.argv) > 2:
    server = sys.argv[2]
else:
    server = TcpSender.def_host

if len(sys.argv) > 3:
    msg = sys.argv[3].encode('utf-8')
else:
    msg = TcpSender.def_msg

if repeat:
    print('Send {0} messages to {1}'.format(repeat, server))
    s = TcpSender()
    s.connect(host=server)

    for i in range(0, repeat):
        print('Send: {}'.format(i))
        s.send(msg)
        time.sleep(0.1)
    s.sink_socket.close()
