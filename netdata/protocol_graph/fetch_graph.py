#!/home/ec2-user/anaconda3/bin/python

import sys
import networkx
from netdata.defaults import database
from netdata.fetch import ProtocolGraph, DateTime, start_end_epoch


def main():
    db = ProtocolGraph(database.host, database.user, database.dbname)

    params = 'parameters: all | frame date time interval_seconds | \
iterall sim | iter sim interval'
    if len(sys.argv) < 2:
        print(params)
        quit()

    if sys.argv[1] == 'all':
        g = db.fetch_all()
        ec = networkx.in_degree_centrality(g)
        print(ec)
    elif sys.argv[1] == 'frame' and len(sys.argv) >= 5:
        date_str = sys.argv[2]
        time_str = sys.argv[3]
        secs = int(sys.argv[4])
        start = DateTime(date_str=date_str, time_str=time_str)
        g = db.fetch_frame(start, seconds=secs)
        ec = networkx.in_degree_centrality(g)
        print(ec)
    elif sys.argv[1] == 'iterall' and len(sys.argv) >= 3:
        sim_name = sys.argv[2]
        print(db.frame(sim_name))
        for g in db.iter(sim_name):
            (start_e, end_e) = start_end_epoch(g)
            print('start: {}, end: {}'.format(start_e, end_e))
            start_dt = DateTime(epoch=start_e)
            print('start utc: {}'.format(str(start_dt)))
            end_dt = DateTime(epoch=end_e)
            print('  end utc: {}'.format(str(end_dt)))
            ec = networkx.in_degree_centrality(g)
            print('In-degree centrality: {}'.format(ec))
    elif sys.argv[1] == 'iter' and len(sys.argv) >= 4:
        sim_name = sys.argv[2]
        print(db.frame(sim_name))
        interval = int(sys.argv[3])
        count = 0
        for g in db.iter(sim_name, seconds=interval):
            print('count: {}'.format(count))
            ec = networkx.in_degree_centrality(g)
            print(ec)
            count += 1
    else:
        print(params)
        quit()


if __name__ == '__main__':
    main()
