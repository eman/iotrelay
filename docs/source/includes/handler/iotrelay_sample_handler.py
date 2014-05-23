# handler/iotrelay_sample_handler.py


class Handler(object):
    def __init__(self, config):
        self.config = config

    def set_reading(self, reading):
        print(reading)
