import psycopg2
import networkx
import logging
import math
from datetime import datetime, timezone


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


def add_record(graph, record):
    """
    Add one record to a graph.
    :params graph: networkx graph.
    :params record: record for an edge.
    :return: graph, as modified in place.
    """
    graph.add_edge(record.sip, record.dip,
                   attr_dict={'sport': record.sport, 'dport': record.dport,
                              'stime_epoch_secs': record.stime_epoch_secs,
                              'etime_epoch_secs': record.etime_epoch_secs})
    return graph


def start_end_epoch(graph):
    """
    Start and end epoch of graph.
    :return: (start epoch, end epoch).
    """
    start = 0
    end = 0
    for e in graph.edges_iter():
        for _, p in graph[e[0]][e[1]].items():
            end = max(end, p['etime_epoch_secs'])
            if start == 0:
                start = p['stime_epoch_secs']
            else:
                start = min(start, p['stime_epoch_secs'])
    return (start, end)


def epoch_utc(s):
    """
    Convert epoch seconds to utc DateTime object.
    :params s: epoch seconds.
    :return: corresponding DateTime object.
    """
    return datetime.fromtimestamp(s, timezone.utc)


class _Frame_Iter:
    """
    Iterator over frames in the protocol graph database.
    """
    _db = None  # ProtocolGraph
    _iter_start = 0  # start epoch for iterating
    _iter_end = -1  # end epoch of time for frames
    _iter_frame_secs = 0  # frame length in seconds for iterating over frames
    _iter_index = 0  # index of the iterator
    _iter_finished = False  # indicates whether iterator is finished

    def __init__(self, db, name, seconds, start, minutes):
        """
        Create iterator with start time over given frame length;
        :param db: ProtocolGraph database.
        :param name: name of the frame
        :param seconds: seconds for the frame;
        :param start: start epoch of iterator; start of dataset if < 0.
        :param minutes: minutes for the frame;
        whole dataset length if minutes and seconds are 0.
        :return: iterator.
        """
        self._db = db

        frame = self._db.frame(name)
        if not frame:
            self._iter_finished = True
        else:
            self._iter_finished = False
            (_, start_epoch, end_epoch, sink_port) = frame
            self._iter_end = end_epoch

            if start >= 0:
                self._iter_start = start
            else:
                self._iter_start = start_epoch

            if minutes == 0 and seconds == 0:
                self._iter_frame_secs = math.ceil(
                    self._iter_end - self._iter_start)
                # print('iter_frame_secs: {}'.format(self._iter_frame_secs))
            else:
                self._iter_frame_secs = minutes * 60 + seconds

    def __iter__(self):
        return self

    def __next__(self):
        if not self._iter_finished:
            start = self._iter_start + self._iter_index * self._iter_frame_secs
            if start <= self._iter_end:
                # print('Fetch frame at {} with {} secs'.format(
                #    str(epoch_utc(start)), self._iter_frame_secs))
                g = self._db.fetch_frame(start, seconds=self._iter_frame_secs)
                self._iter_index += 1
                return g
            else:
                self._iter_finished = True
                raise StopIteration
        else:
            raise StopIteration


class ProtocolGraph:
    """
    Protocol graph obtained from a database with edges.
    Typical usage:
    db = ProtocolGraph(flow_connection)
    g = db.fetch_all()
    or
    for g in db.iter(sim_name, frame_secs)
       process g
    """
    _database = None  # connection to a database

    def __init__(self, flow_connection):
        """
        Initialize with connection.
        :param flow_connection: FlowConnection.
        """
        self._database = flow_connection
        self._database.open()

    def __del__(self):
        """
        Close database if appropriate.
        """
        if self._database:
            self._database.close()

    def fetch_all(self):
        """
        Fetch the whole protocol graph.
        :return: networkx.MultiDiGraph.
        """
        with self._database:
            g = networkx.MultiDiGraph()
            with self._database.cursor() as cur:
                cur.execute("select * from edges;")
                for rec in cur:
                    add_record(g, rec)
        return g

    def fetch_frame(self, start, minutes=0, seconds=0):
        """
        Fetch graph from one frame; include streams that start in the frame.
        :param start: epoch start time.
        :param minutes: minutes for the frame.
        :param seconds: seconds for the frame.
        :return: graph.
        """
        total_secs = minutes * 60 + seconds
        end = start + total_secs
        with self._database:
            g = networkx.MultiDiGraph()
            with self._database.cursor() as cur:
                cur.execute('select * from edges where \
                (%s<=stime_epoch_secs and stime_epoch_secs<%s);',
                            (start, end))
                for rec in cur:
                    add_record(g, rec)
        return g

    def iter(self, name, seconds=0, start=-1, minutes=0):
        """
        Create iterator with start time over given frame length;
        :param name: name of the frame
        :param seconds: seconds for the frame;
        :param start: start epoch of iterator; start of dataset if < 0.
        :param minutes: minutes for the frame;
        whole dataset length if minutes and seconds are 0.
        :return: iterator.
        """
        return _Frame_Iter(self, name, seconds=seconds, start=start,
                           minutes=minutes)
