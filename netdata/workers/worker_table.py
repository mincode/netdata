# Storage for a table of worker instances
# Able to find next available ip address

from ipaddress import IPv4Address
from netdata.workers.list_find import find_first2
from netdata.workers.worker_storage import WorkerStorage


class WorkerTable(WorkerStorage):
    """
    Table of worker instances stored in a json file; 
    consisting of a list of pairs {'ip': ..., 'instance_id': ...};
    able to find next available ip.
    """
    _first_ip = None  # string, first ip number for the storage

    def __init__(self, path, name, first_ip):
        """
        Initizlize.
        :param path: path to the storage file;
        empty means the current direcory.
        :param name: file name, json file.
        :param first_ip: string of first IPv4 address.
        """
        super(WorkerTable, self).__init__(path, name)
        self._first_ip = first_ip

    @property
    def next_index(self):
        """
        Index where to insert the next ip address.
        :return: index such that there is a gap
        between the ips of index-1 and index;
        length of the instance list if none found.
        """
        def p1(x):
            return IPv4Address(self._first_ip) < IPv4Address(x['ip'])

        def p2(x, y):
            return IPv4Address(x['ip'])+1 < IPv4Address(y['ip'])
        return find_first2(self.instances, p1, p2)
 
    def next_ip(self, index):
        """
        Next ip to insert.
        :param index: index where the next ip address is to be inserted.
        :return: next ip address to insert at index.
        """
        if index:
            ip = str(IPv4Address(self.instances[index-1]['ip']) + 1)
        else:
            ip = self._first_ip
        return ip
