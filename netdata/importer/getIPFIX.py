import sys
from ipfix_graph import IPFIXGraph


def main():
    if len(sys.argv)>1:
        ipfix_file = sys.argv[1]
        print('File: ' + ipfix_file)
        ipfix_graph = IPFIXGraph(ipfix_file)
        g = ipfix_graph.fetch_all()
        print("Number of nodes: {}".format(g.number_of_nodes()))
    else:
        print('No file provided!')


if __name__ == '__main__':
    main()
