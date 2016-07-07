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

================================================================  ===================================================
`iotrelay-influxdb <https://github.com/eman/iotrelay-influxdb>`_   A handler for sending data to InfluxDB
`iotrelay-eagle <https://github.com/eman/iotrelay-eagle>`_       Pull data from an Eagle™ Home Energy Gateway
`iotrelay-pywws <https://github.com/eman/iotrelay-pywws>`_       Pull weather data from a weather station via pywws
================================================================  ===================================================

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

    ; ~/.iotrelay.cfg

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

    ; ~/.iotrelay.cfg

    [iotrelay]

    [iotrelay-sample-handler]
    reading types = weather, power, random

This example configuration file would cause the
``iotrelay-sample-hanlder`` to receive data from three reading types:
weather, power, and random. Weather and power reading types are
produced by the plugins referenced earlier: ``iotrelay-pywws`` and
``iotrelay-eagle``. Readings of type ``random`` are produced by the
data source sample plugin shown in the next section.

Data Source Sample Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A data source definition is a class which provides a ``get_reading()``
method and a constructor which accepts a ``config`` parameter. The
``get_reading()`` method must return one or more instances of the
``Reading()`` class or None. In this example,  create a file called
``iotrelay_sample_source.py`` and enter the following code.

.. literalinclude:: includes/source/iotrelay_sample_source.py

IoT Relay uses setuptools to find plugins registered in the
``iotrelay`` group. Data-sources should use the entry-point name
``source``. The following configuration should be placed in
``setup.py`` and in the same directory as
``iotrelay_sample_source.py``.

.. literalinclude:: includes/source/setup.py

Install the source plugin by typing:

.. code-block:: bash

    $ python setup.py install

Data Handler Sample Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Like the previous example, create a new directory with two files:

.. literalinclude:: includes/handler/iotrelay_sample_handler.py

.. literalinclude:: includes/handler/setup.py

Install the handler plugin by typing:

.. code-block:: bash

    $ python setup.py install
