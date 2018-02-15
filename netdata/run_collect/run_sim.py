#!/home/ec2-user/anaconda3/bin/python
# needs to be run with sudo for using port 80

import sys
import os
import json
import time
import zmq
import logging
from netdata.workers import sender_instance, sink_instance
from netdata.workers import WorkerStorage
from netdata.workers import get_home_dir
from netdata.workers import JSONStorage


def log_info(msg):
    """
    Print info log message.
    :params msg: message text.
    """
    logging.info('Control:  ' + msg)


def log_debug(msg):
    """
    Print debug log message.
    :params msg: message text.
    """
    logging.debug('Control: ' + msg)


class TcpController:
    """Send control strings.
    """
    def_msg_dict = {'function': 'echo', 'params': {}}  
    # default message to send
    def_port = 2323  # default port
    def_log_file = '/tmp/controller_log.txt'

    ctrl_context = None  # zmq.Context
    ctrl_socket = None  # a socket

    def __init__(self):
        """
        Initialize as stream socket.
        :param log_file: log file; none if empty.
        """
        self.ctrl_context = zmq.Context()
        self.ctrl_socket = self.ctrl_context.socket(zmq.REQ)

    def connect(self, host, port=def_port):
        log_info('connect to {0}:{1}'.format(host, port))
        self.ctrl_socket.connect('tcp://{0}:{1}'.format(host, port))

    def send(self, msg_dict=def_msg_dict):
        msg = json.dumps(msg_dict).encode('utf-8')
        self.ctrl_socket.send(msg)
        log_debug('expecting echo')
        data = self.ctrl_socket.recv()
        log_info('send-reply done')
        log_debug("received data: " + str(data, 'utf-8'))


def count_sink_groups(sim):
    """
    Count up to what number a dict has
    consecutive members "0", "1", "2", etc.
    :param sim: simulation dict.
    :return: count.
    """
    count = 0
    while True:
        if str(count) in sim.data:
            count += 1
        else:
            break
    return count


def server_programs(sim, sink_ips, sink_port):
    """
    Get list of server programs for sinks.
    :param sim: simulation dict.
    :param sink_ips: list of sink ips.
    :param sink_port: port used by the sinks.
    :return: dict with sink_index: server_program.
    """
    servers = dict()
    for item, program in sim.data.items():
        examine = item.split('server')
        if len(examine) > 1:
            if not examine[0]:
                try:
                    index = int(examine[1])
                except:
                    index = -1
            if index >= 0:
                p = program.copy()
                sinks = [[sink_ips[sink[0]], sink_port, sink[1]]
                         for sink in program['sinks']]
                p['sinks'] = sinks

                servers[index] = p
    return servers


def hit_list(hits, sink_ips, sink_port):
    """
    Convert a list of hit indices or ranges into a list of [ip, port].
    :param hits: list of sink indices or
    pairs [range_start, range_end] of ranges of indices.
    :param sink_ips: list of sink ips.
    :param sink_port: port used by the sinks.
    :return list of [ip, port].
    """
    hit_ips = list()
    for i in hits:
        if isinstance(i, list):
            for j in range(i[0], i[1]+1):
                hit_ips.append([sink_ips[j], sink_port])
        else:
            hit_ips.append([sink_ips[i], sink_port])
    return hit_ips

     
def params_list(sim, sink_ips, sink_port):
    """
    Convert a simulation dict into a list of params to be run by the senders.
    :param sim: simulation dict.
    :param sink_ips: list of sink ips.
    :param sink_port: port used by the sinks.
    :return list of params dict
    """
    params = {'duration': sim.get('duration'), 'step': sim.get('step')}
    if 'start' in sim.data:
        params['start'] = sim.get('start')
    else:
        params['start'] = 0

    l = []
    groups = count_sink_groups(sim)
    for i in range(groups):
        p = params.copy()
        log_debug('senders & sinks: ' + str(sim.get(str(i))))
        program = sim.get(str(i))
        p['emit_prob'] = program['emit_prob']
        p['senders'] = program['quantity']
        p['burst'] = program['burst']
        sinks = [[sink_ips[sink[0]], sink_port, sink[1]]
                 for sink in program['sinks']]
        p['sinks'] = sinks
        if 'hits' in program:
            p['hits'] = hit_list(program['hits'], sink_ips, sink_port)
        else:
            p['hits'] = list()
        l.append(p)
    return l


def main_message():
    print('Parameters: <simulation file> [debug | dry]')
    print('debug = enable debug logging')
    print('dry = dry run and debug logging')
    print('or: <target ip> <quit|abort>')


def main():
    if len(sys.argv) < 2:
        main_message()
        quit()

    if len(sys.argv) == 2 or sys.argv[2] in ['debug', 'dry']:
        simulation = True
        sim_file = sys.argv[1]
        if not os.path.isfile(sim_file):
            sim_file = 'sims/' + sim_file + '.json'
            if not os.path.isfile(sim_file):
                main_message()
                quit()
        if len(sys.argv) > 2 and sys.argv[2] in ['debug', 'dry']:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
    else:
        simulation = False
        if len(sys.argv) < 3:
            main_message()
            quit()
        log_level = logging.DEBUG
        server = sys.argv[1]
        function = sys.argv[2]

    log_file = TcpController.def_log_file
    if log_file:
        logging.basicConfig(filename=log_file, filemode='w', level=log_level)

    if not simulation:
        log_info('function: ' + function)
        sender_ips = [server]
        params = {}
        log_info('parameters: ' + str(params))

        for h in sender_ips:
            s = TcpController()
            s.connect(host=h)
            msg_dict = {'function': function, 'params': params}
            s.send(msg_dict)
        s.ctrl_socket.close()

    else:  # run simulation
        log_info('simulation: ' + sim_file)
        sim = JSONStorage('', sim_file)
        lag = 2.0
        sink_port = sim.sink_port  # 5005 usually

        save_dir = os.path.join(get_home_dir(),
                                sender_instance['table_dir'])
        sink_ips = WorkerStorage(save_dir,
                                 sink_instance['storage']).all_ips
        log_debug('sink_ips: ' + str(sink_ips))

        programs = params_list(sim, sink_ips, sink_port)
        # dict with senders and sinks

        sender_ips = WorkerStorage(save_dir,
                                   sender_instance['storage']).all_ips
        log_debug('sender_ips: ' + str(sender_ips))

        start_index = 0
        start = time.time() + lag
        for p in programs:
            end_index = start_index + p['senders']
            log_info('sender index range {0} - {1}'.
                     format(start_index, end_index-1))
            p['start'] = start
            log_debug('params: ' + str(p))
            for i in range(start_index, end_index):
                log_debug('send to {0}: {1}'.format(i, sender_ips[i]))
                s = TcpController()
                if len(sys.argv) < 3 or sys.argv[2] != 'dry':
                    s.connect(host=sender_ips[i])
                    msg_dict = {'function': 'send', 'params': p}
                    s.send(msg_dict)
            start_index = end_index

        servers = server_programs(sim, sink_ips, sink_port)
        log_debug('processing servers, if any')
        for i, p in servers.items():
            p['start'] = start
            log_debug('server params: ' + str(p))
            log_debug('send to {0}: {1}'.format(i, sink_ips[i]))
            s = TcpController()
            if len(sys.argv) < 3 or sys.argv[2] != 'dry':
                s.connect(host=sink_ips[i])
                msg_dict = {'function': 'send', 'params': p}
                s.send(msg_dict)
            
        sim.set('start', start)


if __name__ == '__main__':
    main()
