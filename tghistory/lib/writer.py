#
import logging

LOG = logging.getLogger('tgh.lib.writer')


class Writer(object):

    def __init__(self, me, contact, args, config):
        self.me = me
        self.contact = contact
        self.args = args
        self.config = config

    def _get_folder(self, contact):
        pass

    def write_lines(self, lines):
        """
        """
        for line in lines:
            print(line)

    def write_line(self, line):
        pass
