#!/home/ec2-user/anaconda3/bin/python

# Import data from a sim into the database.

import logging
import os
import sys
import silk
import psycopg2
from netdata.run_collect import SimProgram, silk_str, epoch_utc


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


def in_time_frame(sim_start_epoch, sim_end_epoch,
                  rec_start_epoch, rec_end_epoch):
    """
    Check wheter record is inside the simulation time frame.
    :param sim_start_epoch: simluation start.
    :param sim_end_epoch: simulation end.
    :param rec_start_epoch: record start.
    :param rec_end_epoch: record end.
    :return: True if record overlaps with the simulation time frame.
    """
    outside = (rec_end_epoch <= sim_start_epoch or
               sim_end_epoch <= rec_start_epoch)
    return not outside


def main():
    if silk.get_configuration('TIMEZONE_SUPPORT') != 'UTC':
        print('silk must be configured for UTC')
        quit()

    if len(sys.argv) < 2:
        print('Parameters: <simulation file> [any string for debug]')
        quit()

    if len(sys.argv) > 2:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)

    sim_file = sys.argv[1]
    if not os.path.isfile(sim_file):
        sim_file = 'sims/' + sim_file + '.json'

    sim = SimProgram(sim_file)
    log_info('Sim: {}'.format(sim.short_name))

    silk.site.init_site()
    log_debug('start: {}'.format(silk_str(sim.start_utc)))
    log_debug('  end: {}'.format(silk_str(sim.end_utc)))

    log_info('Sim {} epoch: {} - {}'.
             format(sim.short_name,
                    sim.start_epoch, sim.end_epoch))
    log_info('Sim {} utc: {} - {}'.
             format(sim.short_name,
                    sim.start_utc, sim.end_utc))

    it = silk.site.repository_iter(start=silk_str(sim.start_utc),
                                   end=silk_str(sim.end_utc),
                                   classtypes=('all', 'ext2ext'))

    conn = psycopg2.connect("host=db0.chgate.net user=analyzer dbname=graphs")
    cur = conn.cursor()

    min_stime = 0
    max_etime = 0
    for file in it:
        log_info('data file: {}'.format(file))
        fh = silk.silkfile_open(file, silk.READ)

        count = 0
        dport_eq_sink_port = 0
        for rec in fh:
            count += 1
            if rec.dport == sim.sink_port:
                dport_eq_sink_port += 1
                log_info('records processed: {0}, dport == sink_port: {1}'.
                         format(count, dport_eq_sink_port))
                if in_time_frame(sim.start_epoch, sim.end_epoch,
                                 rec.stime_epoch_secs, rec.etime_epoch_secs):
                    log_info('valid record')
                    record_start = rec.stime_epoch_secs \
                                   if sim.start_epoch <= rec.stime_epoch_secs \
                                   else sim.start_epoch
                    if rec.stime_epoch_secs < sim.start_epoch:
                        log_info('There is a record starting before sim.start: {}'.
                                 format(count))
                    cur.execute('insert into edges \
                    (sip, sport, dip, dport, \
                    stime_epoch_secs, etime_epoch_secs)\
                    values (%s, %s, %s, %s, %s, %s);',
                                (str(rec.sip), rec.sport,
                                 str(rec.dip), rec.dport,
                                 record_start, rec.etime_epoch_secs))
                    print('etime: {}'.format(rec.etime_epoch_secs))
                    if min_stime == 0:
                        min_stime = record_start
                    else:
                        min_stime = min(min_stime, record_start)
                    max_etime = max(max_etime, rec.etime_epoch_secs)
        conn.commit()

    cur.execute('insert into frames (frame, start_epoch, end_epoch, sink_port) \
    values (%s, %s, %s, %s);',
                (sim.short_name, min_stime, max_etime,
                 sim.sink_port))
    log_info('Recorded epoch: {} - {}'.
             format(min_stime, max_etime))
    log_info('Recorded utc: {} - {}'.
             format(epoch_utc(min_stime), epoch_utc(max_etime)))
    # log_info('Sim start == rec start: {}'.format(sim.start_epoch == min_stime))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
