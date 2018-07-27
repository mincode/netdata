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

### Control Workers

netdata/workers/ctrl_ami is the Python script that counts, launches, starts, stops and terminates
sink and sender machines.

To see the command line parameters run:

    ctrl_ami

Workers may either act as senders that send random messages or sinks that receive messages.

To launch <num> new instances of sender or sink workers:

    ctrl_ami <senders|sinks> launch <num>

To start, stop and terminate senders or sinks use:

    ctrl_ami <senders|sinks> start
    ctrl_ami <senders|sinks> stop
    ctrl_ami <senders|sinks> terminate

### Run Network Simulations

Each network simulation is specified by a configuration file, described by netdata/run_collect/sim_format.txt.
Sample configurations can be found in netdata/run_collect/sims.
Before running a simulation laucnh the appropriate number of sender and sink workers. The scripts for running simulations are
contained in netdata/run_collect/.

To run the simulation, execute:

    run_sim <simulation configuration file>

### Collect Network Communication Data

Network communication data is stored in the postgres database for further analysis.
The data comprises of standard information about IPFIX network flows derived from the messages exchanged between the sender and sink
workers, such as source and destinatin ip addresses,
ports, start and end times, etc.
The scripts for running simulations are
contained in netdata/run_collect/.

To import the data into the database, run:

    get_sim_results <simulation configuration file>

### Analyze Network Communication Data

The ProtocolGraph class from netdata/protocol_graph/protocol_graph.py represents the data from a network simulation.
The flow data can be accessed as a [NetworkX](https://networkx.github.io/) multidigraph (multi-graph with directed edges), where the nodes are the worker nodes
and the edges represent IPFIX flows. Create A new ProtocolGraph object with

     db = ProtocolGraph(host, user, dbname)

where host, user and dbnmae is the ip address of the database sever, database user name and respectively database name with the
flow data.

Iterate over the graphs obtained from a simulation for consecutive time frames of length frame_sec with

  db.iter(sim_name, frame_sec)

where sim_name is the name of the simulation as defined by the simulation configuration file.

See the script connected_components.py as an example for analyzing the connected components
of a graph obtained from a simulation.

### Import IPFIX Flow Data

While the script get_sim_results described above imports network flow data from SiLK, netdata/import contains tools for accessing
network flows saved in IPFIX files directly without storing the data in the database server. The file ipfix_graph.py
implements IPFIXGraph to access IPFIX files as simulation data via ProtocolGraph.

To create an IPFIXGraph object, use

    IPFIXGraph(ipfix_file)

where ipfix_file is the name of the IPFIX data file.

The script getIPFIX illustrates the use of IPFIXGraph.

## Resources
- [SiLK website](https://tools.netsa.cert.org/silk/index.html)
- [yaf website](https://tools.netsa.cert.org/yaf/libyaf/index.html)
- [PostgreSQL](https://www.postgresql.org/)
- [NetworkX](https://networkx.github.io/)
