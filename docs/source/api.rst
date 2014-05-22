API Documentation
=======================================================================

.. py:class:: iotrelay.Reading(reading_type, value[, timestamp[, series_key]])

    Reading provides a container for passing a datum, or "Reading",
    between sources and handlers.

    .. py:attribute:: reading_type

        The reading type represents a category of readings.
        For eaxmple, a weather station might produce temperature,
        rainfall, and windspeed. Because all of these are related to
        weather, they could be categorized with a reading type of
        "weather". ``reading_type`` is used to match data sources with
        data handlers. If a data source generates readings with a
        ``reading_type`` of weather, data handlers that have registered
        an interest in weather will receive those readings.

    .. py:attribute:: value

        contains the datum being communicated.

    .. py:attribute:: timestamp

        A a datetime.datatime object containing the timestamp at which
        the reading was taken.

        If no timestamp is specified in the constructor, timestamp is
        set to the time the Reading object was created.

    .. py:attribute:: series_key

        identifies an individual time series. A weather station may
        produce multiple data streams, one for each sensor.
        Each of these streams should have their own series key.

        If a ``series_key`` is not specified in the constructor,
        ``series_key`` is set to ``reading_type``.

.. py:class:: DataSource(config)

    DataSource is an abstract class for implementing data source plugins.

    .. py:attribute:: config

        A dict containing key/value pairs corresponding to options taken
        from the plugin's section in iotrelay's config file,
        ``~/.iotrelay.cfg``.

    .. py:function:: get_readings

        Get readings from a data source.

        :return: one or more Readings or no Reading
        :rtype: Reading, an iterator of Readings, or None

Example Data Source

.. code-block:: python

    import random
    from iotrelay import Reading


    class DataSource(object):
        def __init__(self, config):
            self.config = config

        def get_readings(self):
            return Reading(reading_type='sample', value=random.randint(1, 100))


.. py:class:: Handler(config)

    Handler is an abstract class for implementing data handler plugins.

    .. py:attribute:: config

        A dict containing key/value pairs corresponding to options taken
        from the plugin's section in iotrelay's config file,
        ``~/.iotrelay.cfg``.

    .. py:function:: set_reading(reading)

        Send a reading to a handler.

    :param iotrelay.Reading reading: The Reading instance being sent to the
        handler.

    .. py:function:: flush()

        *Optional*: Flush any readings that have not been send or otherwise
        processed.

Example Data Handler

.. code-block:: python

    class Handler(object):
        def __init__(self, config):
            self.config = config

        def set_reading(self, reading):
            print(reading)
