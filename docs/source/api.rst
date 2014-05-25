API Documentation
=======================================================================

.. py:module:: iotrelay

Constants
-----------------------------------------------------------------------

.. data:: version

    The version number of the iotrelay module, as a string.

.. data:: DEFAULT_CONFIG

    The configuration file name and path to use if one is not specified.

.. data:: GROUP

    The setuptools group to inspect for available plugins.

Classes
------------------------------------------------------------------------

.. py:class:: Reading(reading_type, value[, timestamp[, series_key]])

    Reading provides a container for passing a datum, or "Reading",
    between sources and handlers.

    .. py:attribute:: reading_type

       represents a category of readings. For example, a weather
       station might produce temperature, rainfall, and wind speed.
       Because all of these are related to weather, they could be
       categorized with a reading type of "weather".
       :attr:`reading_type` is used to match data sources with data
       handlers. If a data source generates readings with a
       :attr:`reading_type`  of weather, data handlers that have
       registered an interest in weather will receive those readings.

    .. py:attribute:: value

       contains the datum being communicated.

    .. py:attribute:: timestamp

       A a :mod:`datetime` object containing the
       time stamp at which the reading was taken.

       If timestamp is not specified in the constructor, timestamp is
       set to the time the :py:obj:`Reading` object was created.

    .. py:attribute:: series_key

       identifies an individual time series. A weather station may
       produce multiple data streams, one for each sensor.
       Each of these streams should have their own series key.

       If a :attr:`series_key` is not specified in the constructor,
       :attr:`series_key` is set to :attr:`reading_type`.

.. py:class:: DataSource(config)

    DataSource is an abstract class for implementing data source plugins.

    .. py:attribute:: config

       A dict containing key/value pairs corresponding to options taken
       from the plugin's section in iotrelay's config file,
       ``~/.iotrelay.cfg``.

    .. py:method:: get_readings

       Get readings from a data source.

       :return: one or more Readings or no :py:class:`Reading`
       :rtype: :py:class:`Reading`, an iterable of :py:class:`Reading`
           instances, or None

    Example Data Source:

    .. literalinclude:: includes/source/iotrelay_sample_source.py

.. py:class:: Handler(config)

    Handler is an abstract class for implementing data handler plugins.

    .. py:attribute:: config

       A dict containing key/value pairs corresponding to options taken
       from the plugin's section in iotrelay's config file,
       ``~/.iotrelay.cfg``.

    .. py:method:: set_reading(reading)

       Send a reading to a handler.

       :param iotrelay.Reading reading: The Reading instance being sent
           to the handler.

    .. py:function:: flush()

       *Optional*: Flush any readings that have not been sent or otherwise
       processed.

    Example Data Handler:

    .. literalinclude:: includes/handler/iotrelay_sample_handler.py
