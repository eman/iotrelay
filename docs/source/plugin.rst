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

Available Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================================================  ===================================================
`iotrelay-tempodb <https://github.com/eman/iotrelay-tempodb>`_   A handler for sending data to TempoDB              
`iotrelay-eagle <https://github.com/eman/iotrelay-eagle>`_       Pull data from an Eagle Home Energy Gateway        
`iotrelay-pywws <https://github.com/eman/iotrelay-pywws>`_       Pull weather data from a weather station via pywws 
===============================================================  ===================================================

Plugin Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each plugin will typically have its own configuration options. All
plugins share the same .iotrelay.cfg configuration file. On plugin
initialization, each plugin is provided with the options contained in
its section.

Each plugin must at least be represented by a section in the
configuration file. If no section exists for a given plugin, it is
assumed to be disabled.

Plugin section names match the plugin name. For example, the following
configuration file would enable (but not necessarily configure) the
iotrelay-sample-source and iotrelay-sample-handler plugins.

.. code-block:: ini

    [iotrelay]
    [iotrelay-sample-source]
    [iotrelay-sample-handler]
    
Handler plugins must list the types of readings they're interested in.
If a ``reading_type`` for a handler plugin is left unset, that plugin
will not receive any readings. The following example shows that the
iotrelay-sample-handler is interested in receiving weather and power
readings. Note that this handler may receive more than two time series
with this configuration. Reading type represents a category of possible
readings.

.. code-block:: ini

    [iotrelay]
    [iotrelay-sample-handler]
    reading types = weather, power


Data Source Sample Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A data source definition is a class which provides a ``get_reading()``
method and a constructor which accepts a ``config`` parameter. The
``get_reading()`` method must return one or more instances of the
``Reading()`` class or None. In this example,  create a file called
``iotrelay_sample_source.py`` and enter the following code.

.. code-block:: python

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

``iotrelay_sample_handler.py``

.. code-block:: python

    class Handler(object):
        def __init__(self, config):
            self.config = config

        def set_reading(self, reading):
            print(reading)

``setup.py``

.. code-block:: python

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
