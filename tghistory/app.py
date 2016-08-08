#
import sys
import yaml
import logging
import argparse
from os import path
from addict import Dict

from tghistory.lib.singleton import Singleton
from tghistory.lib.telegram import TelegramHistory

logging.basicConfig(format='%(asctime)s - '
                           '%(name)s:%(lineno)d - '
                           '%(levelname)s - %(message)s',
                    level=logging.DEBUG)

pytg_log = logging.getLogger('pytg').setLevel(logging.INFO)
pytg_log = logging.getLogger('pytg.sender').setLevel(logging.ERROR)

LOG = logging.getLogger('tgh.app')


class App(object, metaclass=Singleton):

    def __init__(self):
        self._args = None
        self._config = None

        self.tg = TelegramHistory(self.args, self.config)

    @property
    def args(self):
        if self._args:
            return self._args

        parser = argparse.ArgumentParser()
        parser.add_argument('--conf', default='config.yml')
        parser.add_argument('--contact', default=None,
                            help='Dump history for only a single client')
        parser.add_argument('--log-level', default='DEBUG')
        parser.add_argument('--test-mode', default=False, action='store_true')
        self._args = parser.parse_args()
        return self._args

    @property
    def config(self):
        """
        :rtype: dict
        """
        if self._config:
            return self._config

        file = self.args.conf
        LOG.info('Looking for %s' % file)

        # search each directory going up one dir at a time
        dirs = path.split(path.abspath(__file__))
        dirs = path.split(dirs[0])
        while dirs:
            if dirs[0] == '/' and not dirs[1]:
                break

            fpath = '/'.join(dirs) + '/' + file
            dirs = path.split(dirs[0])

            try:
                with open(fpath) as f:
                    config = yaml.load(f)
                    self._config = Dict(config)
                    LOG.info('Config %s loaded' % fpath)
                    break
            except NotADirectoryError:
                continue
            except FileNotFoundError:
                continue
            except Exception as e:
                LOG.exception(e)
                exit(-1)

        return self._config

    def main(self):
        """

        """
        self.tg.run()

    def run(self):
        self.main()
