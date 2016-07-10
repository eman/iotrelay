'''
Copyright (c) 2016, Emmanuel Levijarvi
All rights reserved.
License BSD

iotrelay.py provides an application and a framework for passing data
between data sources and handlers.
'''
import argparse
import datetime
from collections import defaultdict
import pkg_resources
import os
import sys
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
version = "1.2.0"


class Error(Exception):
    pass


class PluginError(Error):
    pass


class ConfigParser(configparser.SafeConfigParser):
    '''ConfigParser is a subclass of the standard library's ConfigParser.

    It adds the ability to parse an option as a list. See the Python
    Standard Library Documentation for more.
    '''
    @staticmethod
    def _make_list(value, sep):
        return [v.strip() for v in value.split(sep)]

    def getlist(self, section, option, sep=','):
        '''Parse an option as a list, optionally specifying the separator
        by specifying the sep argument.
        '''
        return self._make_list(self.get(section, option), sep)


class Reading(object):
    '''Reading provides a container for passing a datum,or "Reading",
    between sources and handlers.

    Attributes:
        reading_type (str):
        value (str):
        timestamp (datetime.datetime):
        series_key (str):
    '''
    def __init__(self, reading_type, value, timestamp=None, series_key=None,
                 tags=None):
        self.reading_type = reading_type
        self.value = value
        self.series_key = series_key
        if series_key is None:
            self.series_key = reading_type
        if timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        else:
            self.timestamp = timestamp
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
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
        return "{0}: {1!s}, {2!s}".format(self.timestamp.isoformat(),
                                          self.series_key,
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
        logger.debug('IoTrelay loading plugins')
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
                try:
                    reading_types = self.config.getlist(plugin_name,
                                                        'reading types')
                except configparser.NoOptionError:
                    msg = "No 'reading types' specified for handler {0}"
                    logger.warning(msg.format(plugin_name))
                else:
                    for reading_type in reading_types:
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
                try:
                    readings = source.get_readings()
                except PluginError as e:
                    logger.error('Unable to read from source. {0}'.format(e))
                    continue
                if readings is None:
                    continue
                for reading in readings:
                    for handler in self.handlers.get(reading.reading_type, []):
                        if reading.value is None:
                            logger.warning('None value from {0}'.format(
                                reading.series_key))
                            continue
                        try:
                            handler.set_reading(reading)
                        except PluginError as e:
                            logger.error('Unable to send data {0}'.format(e))
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
    logging.basicConfig(format='%(asctime)s %(message)s',
                        level=args.log_level.upper())
    config = ConfigParser()
    if args.config_file is None:
        config_file = DEFAULT_CONFIG
    else:
        config_file = args.config_file
    try:
        f = open(config_file, 'r')
    except IOError as e:
        logger.critical("Cannot open config file {0}. {1}.".format(e.filename,
                                                                   e.strerror))
        sys.exit(1)
    with f:
        config.readfp(f)
    r = Relay(config)
    r.load_plugins()
    r.run()
    r.flush_handlers()


if __name__ == "__main__":
    main()
