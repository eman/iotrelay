'''
Copyright (c) 2014, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import argparse
import datetime
from collections import defaultdict
import pkg_resources
import os
import signal
import threading
import logging
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

logger = logging.getLogger()

DEFAULT_CONFIG = os.path.join(os.path.expanduser("~"), '.iotrelay.cfg')
GROUP = 'iotrelay'
__version__ = "1.0.0"


class ConfigParser(configparser.SafeConfigParser):
    @staticmethod
    def _make_list(value, sep):
        return [v.strip() for v in value.split(sep)]

    def getlist(self, section, option, sep=','):
        return self._make_list(self.get(section, option), sep)


class Reading(object):
    def __init__(self, reading_type, value, timestamp=None, series_key=None):
        self.reading_type = reading_type
        self.value = value
        self.series_key = series_key
        if series_key is None:
            self.series_key = reading_type
        if timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        else:
            self.timestamp = timestamp
        self.iteration = False

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.iteration:
            raise StopIteration
        self.iteration = True
        return self

    def __str__(self):
        return "{0}: {1!s}, {2!s}".format(self.series_key,
                                          self.timestamp.isoformat(),
                                          self.value)

    def __repr__(self):
        return ("Reading({self.reading_type!r}, {self.value!r}, "
                "{self.timestamp!r}, {self.series_key!r})".format(self=self))


class Relay(object):
    def __init__(self, config):
        self.config = config
        self.stop_event = threading.Event()
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        self.sources = []
        self.handlers = defaultdict(list)

    def load_plugins(self):
        for entrypoint in pkg_resources.iter_entry_points(group=GROUP):
            plugin_name = entrypoint.dist.project_name
            try:
                plugin_config = dict(self.config.items(plugin_name))
            except configparser.NoSectionError:
                logging.warning('Plugin: {0} not loaded. It has not been '
                                'configured.'.format(plugin_name))
                continue
            plugin = entrypoint.load()(plugin_config)
            if entrypoint.name == 'handler':
                for reading_type in self.config.getlist(plugin_name,
                                                        'reading_types'):
                    self.handlers[reading_type].append(plugin)
            elif entrypoint.name == 'source':
                self.sources.append(plugin)
            logger.debug("Plugin: {0}.{1}, loaded".format(plugin_name,
                                                          entrypoint.name))

    def stop(self, signum, stack):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            for source in self.sources:
                for reading in source.get_readings():
                    for handler in self.handlers.get(reading.reading_type, []):
                        if reading.value is None:
                            logger.warning('None value from {0}'.format(
                                reading.series_key))
                            continue
                        handler.set_reading(reading)
            self.stop_event.wait(1)

    def flush_handlers(self):
        flushed = set()
        for handler_list in self.handlers.values():
            for handler in handler_list:
                if handler in flushed:
                    continue
                try:
                    handler.flush()
                except AttributeError:
                    pass
                flushed.add(handler)


def main():
    parser = argparse.ArgumentParser(description="Internet of Things Relay")
    parser.add_argument('-c', '--config-file', help="Configuration Filename")
    parser.add_argument('--log-level', help="Log Level", default='info',
                        choices=('debug', 'info', 'warning', 'info'))
    args = parser.parse_args()
    config = ConfigParser(allow_no_value=True)
    if args.config_file is None:
        config_file = DEFAULT_CONFIG
    else:
        config_file = args.config_file
    with open(config_file, 'r') as f:
        config.readfp(f)
    logging.basicConfig(format='%(message)s', level=args.log_level.upper())
    r = Relay(config)
    r.load_plugins()
    r.run()
    r.flush_handlers()


if __name__ == "__main__":
    main()
