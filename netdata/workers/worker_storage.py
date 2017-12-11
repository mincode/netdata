# Storage for a table of worker instances

from netdata.workers.json_storage import JSONStorage


class WorkerStorage(JSONStorage):
    """
    Table of worker instances stored in a json file; 
    consisting of a list of pairs {'ip': ..., 'instance_id': ...}
    """
    _instances_label = 'instances'  # label in the dict to store the list of {'ip': ip_string, 'instance_id': id_string}

    def __init__(self, path, name):
        """
        Initizlize.
        :param path: path to the storage file; empty means the current direcory.
        :param name: file name, json file.
        """
        super(WorkerStorage, self).__init__(path, name)
        if self._instances_label not in self.data:
            self.set(self._instances_label, [])

    @property
    def instances(self):
        """
        List of instances.
        :return list of {'ip':..., 'instance_id':....}
        """
        return self.get(self._instances_label)

    @property
    def all_ids(self):
        """
        List all instance ids.
        :return list of all instance ids.
        """
        return list(map(lambda x: x['instance_id'], self.instances))

    @property
    def all_ips(self):
        """
        List all instance ips.
        :return list of all instance ips.
        """
        return list(map(lambda x: x['ip'], self.instances))
 
    def insert(self, index, ip, instance_id):
        """
        Insert new instance at given index.
        :param index: index to insert at.
        :param ip: ip address of new instance.
        :param instance_id: id of new instance.
        """
        new_instance = {'ip': ip, 'instance_id': instance_id}
        if index == len(self.instances):
            self.instances.append(new_instance)
        else:
            self.instances.insert(index, new_instance)
        self.dump()

    def delete(self, index):
        """
        Delete entry.
        :param index: index of entry to be deleted.
        """
        del self.instances[index]
        self.dump()

    def delete_all(self):
        """
        Delete all entries.
        """
        self.set(self._instances_label, [])
