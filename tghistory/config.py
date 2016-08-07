#
import yaml
import logging
from os import path

# Using the addict version of Dict, which allows us
# to access the dictionary in a dotted-key syntax
# e.g, instead of config['x']['y'], use config.x.y
from addict import Dict

CONF = None
LOG = logging.getLogger('ftbt.config')


def init(file=None):
    """
    :rtype: dict
    """
    global CONF

    if not file:
        file = 'config.yml'

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
                CONF = Dict(config)

                LOG.info('Config %s loaded' % fpath)
                break
        except NotADirectoryError:
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            LOG.exception(e)
            exit(-1)

    if not CONF:
        LOG.error('Configuration file not found!')
        exit(-1)

    return CONF


def get_config():
    """
    :rtype: dict
    """
    global CONF
    if not CONF:
        LOG.error('No config file loaded')

    return CONF
