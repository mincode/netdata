#!/home/ec2-user/anaconda3/bin/python


import sys
import os
from sim_program import SimProgram, date_time_str, silk_str
from run_sim import count_sink_groups


def count_sinks_senders(sim):
    """
    Count the sinks and senders in a simulation.
    :param sim: simulation dict.
    :return (count sinks, count senders)
    """
    all_sinks = set()
    groups = count_sink_groups(sim)
    count_senders = 0
    for i in range(groups):
        program = sim.get(str(i))
        count_senders += program['quantity']
        sinks = program['sinks']
        sink_set = {sink[0] for sink in sinks}
        all_sinks = all_sinks | sink_set
    return (len(all_sinks), count_senders)


def main():
    # goal is to count all sinks and senders in the simulation
    if len(sys.argv) < 2:
        print('Parameters: <simulation file|name>')
    else:
        sim_file = sys.argv[1]
        if not os.path.isfile(sim_file):
            sim_file = 'sims/' + sim_file + '.json'

        sim = SimProgram(sim_file)

        sim_short = sim.short_name
        print('     sim: ' + sim_short)
        print('Sim file: ' + sim_file)
        sinks, senders = count_sinks_senders(sim)
        print('  sinks: {}'.format(sinks))
        print('senders: {}'.format(senders))


if __name__ == '__main__':
    main()
