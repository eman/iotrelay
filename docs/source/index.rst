IoT Relay: Giving Voice to Your Things
========================================================================
Release |release|

In greater and greater number, "Things" are capable of gathering data
about their environment. These things have an interface to retrieve the
measurements being taken but contain no way of pushing this data to the
Internet. For example, home weather stations often contain only a USB
interface and no network capability. Other devices may have network
capability, such as ZigBee®, but still don't have a direct way to send
data to Internet connected hosts.

Internet of Things Relay is an application and framework for gathering
data from sources and relaying it to destinations. It is somewhat like
publish/subscribe except that it's geared more toward devices that are
unable to initiate a connection (they must be polled to get at their
data).

IoT Relay provides basic setup and matches data sources with interested
handlers. The rest of the work is left to plugins.

Installation
------------------------------------------------------------------------
IoT Relay is available via PyPI.

.. code-block:: bash

    $ pip install iotrelay

It is also necessary to create an (initially empty) ini-style
file: ``~/.iotrelay.cfg``.

.. code-block:: ini

    [itorelay]

Now that IoT Relay is installed, add plugins!

Source
------------------------------------------------------------------------
The source for the IoT Relay project is hosted on GitHub.
https://github.com/eman/iotrelay

License
------------------------------------------------------------------------
The IoT Relay project is licensed under The BSD 2-Clause License.

Contents
------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   running
   plugin
   api
