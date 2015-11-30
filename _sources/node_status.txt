***********
node_status
***********

Overview
========

**node_status**, is an alternative to knife's *status* subcommand.  It provides various
output formats, sorting, filtering, and it is very fast, using partial search.


Example Usage
=============

Return status information for all nodes
---------------------------------------
Output format is similar to *knife status*.

.. code-block:: bash

    $ node_status

Return status information for all nodes with **web** in their name
------------------------------------------------------------------

.. code-block:: bash

    $ node_status -F '*web*'

Return status information for all **healthy** nodes
---------------------------------------------------
Healthy will be considered any node that has had a successful chef-client
run in the past 180 minutes.

.. code-block:: bash

    $ node_status -H -m 180

Return status information for all **healthy** nodes with **db** in their name
-----------------------------------------------------------------------------
Return a list of FQDNs matching our criteria, perhaps for use by fabric.  Sort by
FQDN in ascending order.

.. code-block:: bash

    $ node_status -H -m 180 -f fqdn_list -S fqdn

Display chef-client and ruby version numbers for **healthy** nodes
------------------------------------------------------------------
Sort by ruby version.

.. code-block:: bash

    $ node_status -H -m 180 -f fqdn_list -S ruby_version

Command-line Reference
======================

.. argparse::
   :module: node_status.scripts.cli
   :func: parse_arguments
   :prog: node_status

