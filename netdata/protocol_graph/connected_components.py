#!/home/ec2-user/anaconda3/bin/python

import sys
import re
import networkx as nx
from netdata.protocol_graph.defaults import get_default_db
import decimal


def sink_indices(l):
    """
    Convert list of ips into list of sink indices.
    :param l: list of 10.0.17.* and 10.0.18.* ips where the 17 are the sinks.
    :return: list of indices corresponding to the sinks.
    """
    indices = list()
    for ip in l:
        parts = re.split('\.', ip)
        if parts[2] == '17':
            indices.append(int(parts[3]))
    return indices

    
params = 'parameters: sim_name seconds_per_graph [components | count]\n\
components = print the connected components\n\
count = only print the numbers of the types of connected components'

if len(sys.argv) < 2:
    print(params)
    quit()

sim = sys.argv[1]
# secs = int(sys.argv[2])
secs = decimal.Decimal(sys.argv[2])

if len(sys.argv) > 3:
    print_cc = sys.argv[3] == 'components'
    count_cc = sys.argv[3] == 'count'
else:
    print_cc = False
    count_cc = False


print('sim: {}, secs: {}'.format(sim, secs))

db = get_default_db()
count = 0
num_clusters = dict()
max_clusters = dict()
for g in db.iter(sim, secs):
    if not count_cc:
        print('Graph: {}'.format(count))
    h = g.to_undirected()
    cc = nx.connected_components(h)
    components = list(cc)
    if not count_cc:
        print(components)
    cc_list = list(map(lambda x: sorted(list(x)), components))
    sink_list = list(map(lambda x: sink_indices(sorted(list(x))), components))
    cluster_sizes = sorted(list(map(len, cc_list)))
    if not count_cc:
        print('num clusters: {}'.format(len(cluster_sizes)))
        print('cluster sizes: ', cluster_sizes)
        print('sinks: ', sink_list)
    count_clusters = len(sink_list)
    if cluster_sizes:
        largest = max(cluster_sizes)
    else:
        largest = 0
    if count_clusters in num_clusters:
        num_clusters[count_clusters] += 1
        max_clusters[count_clusters] = max(max_clusters[count_clusters],
                                           largest)
    else:
        num_clusters[count_clusters] = 1
        max_clusters[count_clusters] = largest
    if print_cc:
        print(cc_list)
    count += 1

cluster_counts = sorted(list(num_clusters))
print('Cluster distribution:')
print('num clusters - count of graphs - largest cluster')
for key in cluster_counts:
    print('    {}        -     {}          -      {}'.format(key, num_clusters[key], max_clusters[key]))


