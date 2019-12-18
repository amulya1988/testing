class Momentjs(object):

    def __init__(self, timestamp):
        self.timestamp = timestamp

        # Format time

    def format(self, fmt):
        return self.timestamp.strftime(fmt)
