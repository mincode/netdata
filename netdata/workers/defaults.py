try:
    from workers_defaults import sink_instance, sender_instance
except:
    sink_instance = {
        'ami': 'ami-915394eb',
        'first_ip': '10.0.17.0',
        'security': ['sg-21d88f5c'],  # nosec
        'net_subnet': 'subnet-3557de19',
        'instance_type': 't2.micro',
        'key_name': 'gate',
        'table_dir': 'workers',
        'storage': 'sinks.json',
    }

    sender_instance = {
        'ami': 'ami-ad5b9cd7',
        'first_ip': '10.0.18.0',
        'security': ['sg-21d88f5c'],  # nosec
        'net_subnet': 'subnet-3557de19',
        'instance_type': 't2.micro',
        'key_name': 'gate',
        'table_dir': 'workers',
        'storage': 'senders.json',
    }
