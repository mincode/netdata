# Netdata Python Module

The netdata module is an educational Python module to simulate computer network communications,
collect communication data and analyze the data.

## Installation

To use the module, clone or copy the Python code from the repository. The module requires the network traffic analysis tools
[SiLK](https://tools.netsa.cert.org/silk/index.html) and the PySiLK Python extension.
To use the network simulation functions,
a cloud-based environment must be set up. 

### Install the Network Simulation Functions

## Usage

Simulate and import network flow to derive protocol graphs
starting and stopping worker computers:
go into the directory netdata/workers
(cd netdata/workers)

ctrl_ami is the program that counts, launches, starts, stops and terminates
sink and sender machines.

./ctrl_ami runs the program, and it will show its required parameters.

./ctrl_ami sinks launch 4
launches 4 new instances of "sink" machines
./ctrl_ami senders laucn 4
launches 4 new instances of "sender" machines

./ctrl_ami sinks start
./ctrl_ami sinks stop
starts and stops the sinks. Similarly for "senders".
./ctrl_ami sinks terminate
stops and deletes the sinks.

## Usage
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
- Documentation for the Chat Console
  * [latest version](http://chconsole.readthedocs.org/en/latest/)
  [[PDF](https://media.readthedocs.org/pdf/chconsole/latest/chconsole.pdf)]
  * [stable version](http://chconsole.readthedocs.org/en/stable/)
  [[PDF](https://media.readthedocs.org/pdf/chconsole/stable/chconsole.pdf)]
- [Project Jupyter website](https://jupyter.org)
- [Issues](https://github.com/jupyter/chconsole/issues)
