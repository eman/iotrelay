IoT Relay: Giving Voice to Your Things
========================================================================
Release v1.2.0

In greater and greater numbers, "things" are capable of gathering data
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

Plugins
-----------------------------------------------------------------------
Before IoT Relay can do anything useful, it needs plugins. There are
plugin types: source and handler. Source plugins generate data. Handler
plugins handle or do something with data that source plugins produce.
These definitions are intended to be open-ended. Although IoT Relay was
developed with the intention of relaying time-series type data between
remote sources and remote destinations, a handler could instead view
each datum as an event and trigger some action. Likewise, data source
plugins do not have to simply pass the data they are collecting. They
may process the data in some way before making it available to
interested handlers.

Data Source Sample Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A data source definition is a class which provides a ``get_reading()``
method and a constructor which accepts a ``config`` parameter. The
``get_reading()`` method must return one or more instances of the
``Reading()`` class or None. In this example,  create a file called
``iotrelay_sample_source.py`` and enter the following code.

.. code-block:: python

    # iotrelay_sample_source.py

    import random
    from iotrelay import Reading


    class DataSource(object):
        def __init__(self, config):
            self.config = config

        def get_readings(self):
            return Reading('sample', random.randint(1, 100))

IoT Relay uses setuptools to find plugins registered in the
``iotrelay`` group. Datasources should use the entry-point name
``source``. In the same directory as ``iotrelay_sample_source.py``,
the following code should be placed in ``setup.py``.

.. code-block:: python

    # setup.py

    from setuptools import setup


    setup(name='iotrelay-sample-source',
          install_requires=['iotrelay'],
          py_modules=['iotrelay_sample_source'],
          entry_points={
              'iotrelay': ['source=iotrelay_sample_source:DataSource']
          }
    )

Install the source plugin by typing:

.. code-block:: bash

    $ python setup.py install

Data Handler Sample Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Like the previous example, create a new directory with two files:

.. code-block:: python

    # iotrelay_sample_handler.py

    class Handler(object):
        def __init__(self, config):
            self.config = config

        def set_reading(self, reading):
            print(reading)


    # setup.py

    from setuptools import setup


    setup(name='iotrelay-sample-handler',
          install_requires=['iotrelay'],
          py_modules=['iotrelay_sample_handler'],
          entry_points={
              'iotrelay': ['handler=iotrelay_sample_handler:Handler']
          }
    )

Install the handler plugin by typing:

.. code-block:: bash

    $ python setup.py install

Plugin Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The minimal source plugin used in this example does not require any
configuration. The 'reading types' option in a handler's configuration
specifies which reading types a handler will receive. In order to
receive readings from the 'iotrelay-sample-source' plugin, the
'reading type' option in the iotrelay-sample-handler would be 'sample'.
This corresponds to the reading_type attribute set by the Reading
constructor when get_readings() was called.

The section names correspond directly to the plugin names, as defined
in ``setup.py``.

.. code-block:: ini

    ; ~/.iotrelay.cfg

    [iotrelay]

    [iotrelay-sample-source]
    [iotrelay-sample-handler]
    reading types = sample

Any options specified in each plugins section will be passed to that
plugin's constructor during initialization.

Running IoT Relay
------------------------------------------------------------------------
Start IoT Relay with the following command:

.. code-block:: bash

    $ iotrelay

License
-------------------------------------------------------------------------

IoT Relay is licensed under The BSD 2-Clause License.
