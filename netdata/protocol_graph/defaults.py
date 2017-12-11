from netdata.protocol_graph import ProtocolGraph


__author__ = 'Manfred Minimair <manfred@minimair.org>'

host = 'db0.chgate.net' 
user = 'graph' 
dbname = 'graphs'


def get_default_db():
    db = ProtocolGraph(host, user, dbname)
    return db
