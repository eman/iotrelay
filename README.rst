Internet of Things Relay
=======================================================================
IoT Relay is a framework for connecting many data sources with many
destinations, or handlers. It is intended to be used with time-series,
like those produced by IoT devices, but can probably also be used for
non-time-series data. Handlers register themselves and provide
callbacks, which are invoked when their registered reading type is
received by a data source. A handler may simply relay readings as they
come or it may inspect the readings and generate events based on those
readings.

Creating a data source plugin
=======================================================================
A data source definition is a class which provides a ``get_reading()``
method and a constructor which accepts a ``config`` parameter. The 
``get_reading()`` method must return one or more instances of the
``Reading()`` class or an empty iterator.::

    import random
    from iotrelay import Reading


    class DataSource(object):
        def __init__(self, config):
            self.config = config

        def get_readings(self):
            return Reading('sample', random.randint(1, 100))

IoT Relay uses setup tools to find plugins registered in the
``iotrelay`` group. Datasources should use the entrypoint name
``source``::

    from setuptools import setup


    setup(name='iotrelay-sample-source',
          entry_points={
              'iotrelay': ['source=iotrelay_sample_source:DataSource']
          }
    )

Creating a data handler plugin
=======================================================================
Sample Handler::

    class Handler(object):
       batch_len = 10

        def __init__(self, config):
            self.readings = []
            self.config = config

        def set_reading(self, reading):
            print('set_reading({0!r})'.format(reading))
            if reading is None:
                return
            self.readings.append(reading)
            if len(self.readings) == self.batch_len:
                for item in self.readings:
                    print(item)
                self.readings = []

        def flush(self):
            print('flushing unsent readings')
            for reading in self.readings:
                print(reading)
            self.readings = []

Sample ``setup.py``::

    from setuptools import setup


    setup(name='iotrelay-sample-handler',
          entry_points={
              'iotrelay': ['source=iotrelay_sample_handler:Handler']
          }
    )
