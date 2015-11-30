***************
Getting Started
***************

Installation
============

Prerequisites
-------------

*To get up and running, the following must be installed:*

* python 2.7.x
* pychef
* termcolor

*Other requirements:*

* A working knife configuration, pychef uses ~/.chef/knife.rb

pip
---
From the top-level directory of the cloned repository:

.. code-block:: bash

    pip install .

.. note:: This is typically performed within an active python virtual environment.

And for *optional* document generation with sphinx, install the following python packages as well:

.. code-block:: bash

    pip install sphinx
    pip install pygments
    pip install sphinx_rtd_theme
    pip install sphinx-argparse


Basic Usage
===========

*For a full set of CLI usage examples, please see the* :doc:`node_status` *cli* documentation.
