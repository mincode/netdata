# Netdata Python Module

The netdata module is an educational Python module to simulate computer network communications,
collect communication data and analyze the data.

## Installation

To use the module, clone or copy the Python code from the repository. The module requires the network traffic analysis tools
[SiLK](https://tools.netsa.cert.org/silk/index.html) including the PySiLK Python extension which is used when collecting
and analyzing data.
To use the network simulation functions,
a cloud-based computational environment must be set up. 
Network data can be analyzed without enabling the simulation functions.

### Install the Network Simulation Functions

The network simulation functions use Amazon AWS. Create a subnetwork for worker nodes that are used for sending and receiving
network communications. 

**Workers:**
Create a worker node running Amazon Linux.
Install [yaf](https://tools.netsa.cert.org/yaf/libyaf/index.html)
 on the worker to collect the network comminication data passing to and from the worker.
The appropriate yaf configuration file can be found in netdata/sink/. The worker sends the data to the control host, a host whose ip address
must be set in the yaf configuration file. The host collects the communication data from the workers with the tool rwflowpack from SiLK.
Furthermore, install netdata/send/tcp_sender.py and netdata/sink/tcp_sink.py as daemons on the worker.
Then create an image of it (ami) in Amazon AWS.

**Control Host:**
Create a node running Amazon Linux for the control host. The host must be authorized to launch new EC2 instances in the subnet
running the worker nodes. Furthermore, install 
SiLK and rwflowpack as a service to collect network data from the workers.
Enter the name of the worker ami and the subnet information into netdata/workers/defaults.py. Additinally create the directory
named workers in the home directory of the user who launches workers form the control host.

**Database:**
Communication data is stored in a [PostgreSQL](https://www.postgresql.org/) database. The database must be accessible from the
control host.
Use the script netdata/run_collect/createDatabase create the database and the script netdata/run_collect/createTables to
set up the appropriate tables in the database.
Enter the connection information for the database in netdata/protocol_graph/defaults.py.

## Usage

### Launch Workers

netdata/workers/ctrl_ami is the Python script that counts, launches, starts, stops and terminates
sink and sender machines.

To see the command line parameters run:

    ctrl_ami

Workers may either act as senders that send random messages or sinks that receive messages.

To launch <num> new instances of sink workers:

    ctrl_ami sinks launch <num>

To launch <num> new instances of sender workers:

    ctrl_ami senders laucn <num>


./ctrl_ami sinks start
./ctrl_ami sinks stop
starts and stops the sinks. Similarly for "senders".
./ctrl_ami sinks terminate
stops and deletes the sinks.

To run the Chat Console:

    chconsole

or

    jupyter chconsole

Chat Console can either start its own IPython kernel or
attach to an independent Jupyter kernel, including
 IPython, through a connection file.
For convenience, a script to start an
independent Ipython kernel is included:

    chc-python

**Note:** Make sure that Qt is installed. Unfortunately, Qt cannot be
installed using pip. The next section gives instructions on installing Qt.

## Resources
- [SiLK website](https://tools.netsa.cert.org/silk/index.html)
- [yaf website](https://tools.netsa.cert.org/yaf/libyaf/index.html)
- [PostgreSQL](https://www.postgresql.org/)
