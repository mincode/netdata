#!/home/ec2-user/anaconda3/bin/python


import sys
import os
import logging
from sim_program import SimProgram, date_time_str, silk_str


def log_info(msg):
    """
    Print info log message.
    :params msg: message text.
    """
    logging.info(' ' + msg)


def log_debug(msg):
    """
    Print debug log message.
    :params msg: message text.
    """
    logging.debug(msg)


def main():
    if len(sys.argv) < 2:
        print('Parameters: <simulation file|name>')
    else:
        sim_file = sys.argv[1]
        if not os.path.isfile(sim_file):
            sim_file = 'sims/' + sim_file + '.json'

        logging.basicConfig(
            level=logging.INFO,)
            #level=logging.DEBUG,)

        sim = SimProgram(sim_file)

        sim_short = sim.short_name
        print('     sim: ' + sim_short)
        print('Sim file: ' + sim_file)
        print('Start epoch: {}'.format(sim.start_epoch))
        print('  End epoch: {}'.format(sim.end_epoch))
        start_utc = sim.start_utc
        end_utc = sim.end_utc
        print('\nSilk format start UTC: {}'.format(silk_str(start_utc)))
        print('Silk format   end UTC: {}'.format(silk_str(end_utc)))

        start_est = sim.start_est
        end_est = sim.end_est
        print('\nStart EST: {}'.format(date_time_str(start_est)))
        print('  End EST: {}'.format(date_time_str(end_est)))

        print('\nStart UTC: {}'.format(date_time_str(start_utc)))
        print('  End UTC: {}'.format(date_time_str(end_utc)))

        print('\nDuration: {} sec'.format(sim.duration))
        print('          {} min'.format(sim.duration/60))
        print('          {} hrs'.format(sim.duration/(60*60)))
        print('    Step: {} sec'.format(sim.step))


if __name__ == '__main__':
    main()
