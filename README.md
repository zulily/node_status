node_status
===========
**node_status** is a python script that serves as a knife status replacement, with a number of enhancements.  It
is rather snappy when certain options are used, and leveraging partial search.  Additionally, node_status has various output
formats -- which are particularly useful for generating host lists to be used by fabric scripts.

Documentation
--------------
For the full CLI reference including usage examples, please see [full project documentation](http://zulily.github.io/node_status/).

Prerequisites
--------------

*To get up and running, the following must be installed:*

+ python 2.7.x
+ pychef and its dependencies
+ termcolor

Installation
------------
+ Create a virtual environment and activate
+ Clone this git repository
+ pip install .

*Optionally for sphinx document generation, pip install the following*

+ sphinx
+ pygments
+ sphinx_rtd_theme
+ sphinx-argparse


Example CLI Usage
-----------------
**Display status for all healthy nodes, with 'knife status'-like output**

```bash
node_status
```

License
-------
Apache License, version 2.0.  Please see LICENSE
