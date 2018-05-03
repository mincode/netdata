import networkx
import sys
import os
import silk
from subprocess import Popen
import string
import random


def id_generator(size=8, chars=string.ascii_letters):
    """
    Generate random string.
    size: size of the string to be generated.
    chars: list of letters for the string.
    :return: random string generated.
    """
    L = []
    for _ in range(size):
        L.append(random.choice(chars))
    return ''.join(L)
    # return ''.join(random.choice(chars) for _ in range(size))



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


class IPFIXGraph:
    """
    Protocol graph obtained from a IPFIX file.
    Typical usage:
    db = IPFIXGraph(ipfix_file)
    g = db.fetch_all()
    """
    _silk_file = None  # silk file pipe
    _database = None  # connection to input Silk file


    def connect_db(self, ipfix_file):
        """
        Create a connection to an IPFIX file.
        :param ipfix_file: file name.
        :return: connection.
        """
        self._silk_file = '/tmp/' + os.path.basename(ipfix_file) + id_generator() + '.rw'
        print('Temporary file: ' + self._silk_file)
        os.mkfifo(self._silk_file)
        Popen(['rwipfix2silk', '--silk-output='+self._silk_file, ipfix_file])
        in_file = silk.silkfile_open(self._silk_file, silk.READ)
        return in_file

    def __init__(self, ipfix_file=''):
        """
        Initialize; create connection to IPFIX file
        if file name is provided;
        otherwise no connection created.
        :param ipfix_file: file name of the IPFIX data file.
        """
        if ipfix_file:
            self._database = self.connect_db(ipfix_file)

    def __del__(self):
        """
        Close connection if appropriate.
        """
        if self._database:
            # It seems it is closed automatically.
            # self._database.close()
            os.remove(self._silk_file)
            pass

    def fetch_all(self):
        """
        Fetch the whole protocol graph.
        :return: networkx.MultiDiGraph.
        """
        with self._database:
            g = networkx.MultiDiGraph()
            for rec in self._database:
                add_record(g, rec)
        return g

def main():
    ipfix_file = sys.argv[1]
    print('File: ' + ipfix_file)
    ipfix_graph = IPFIXGraph(ipfix_file)
    g = ipfix_graph.fetch_all()
    print("Number of nodes: {}".format(g.number_of_nodes()))

if __name__ == '__main__':
    main()
