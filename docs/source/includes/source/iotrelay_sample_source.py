# source/iotrelay_sample_source.py

import random
from iotrelay import Reading


class DataSource(object):
    def __init__(self, config):
        self.config = config

    def get_readings(self):
        value = random.randint(1, 100)
        return Reading(reading_type='random', value=value)
