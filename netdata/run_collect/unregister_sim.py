#!/home/ec2-user/anaconda3/bin/python

# delete sim name from frames table

import logging
import os
import sys
import psycopg2
from simulatepg.run_collect import SimProgram


def log_info(msg):
    """
    Print info log message.
    :params msg: message text.
    """
    logging.info(' ' + msg)


def main():
    if len(sys.argv) < 2:
        print('Delete simulation name from table.')
        print('Parameters: <simulation file or sim name>')
        quit()

    log_level = logging.INFO
    logging.basicConfig(level=log_level)

    sim_file = sys.argv[1]
    if not os.path.isfile(sim_file):
        sim_file = 'sims/' + sim_file + '.json'

    sim = SimProgram(sim_file)
    log_info('Sim: {}'.format(sim.short_name))

    conn = psycopg2.connect("host=db0.chgate.net user=analyzer dbname=graphs")
    cur = conn.cursor()

    cur.execute('delete from frames where frame=%s', (sim.short_name,))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
