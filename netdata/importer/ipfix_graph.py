from ipfix_connection import IPFIXConnection
from protocol_graph import ProtocolGraph


def IPFIXGraph(ipfix_file):
    """
Access IPFIX data file.
:param ipfix_file: file name of ipfix data.
:return: ProtocolGraph corresponding to the ipfix data.
"""
    connection = IPFIXConnection(ipfix_file)
    ipfix_graph = ProtocolGraph(connection)
    return ipfix_graph
