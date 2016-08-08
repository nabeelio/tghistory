# -*- coding: utf-8 -*-

import logging
from jinja2 import Environment, PackageLoader

from tghistory.lib.singleton import Singleton

LOG = logging.getLogger('tgh.templates')


class Templates(object, metaclass=Singleton):

    def __init__(self):
        super(Templates, self).__init__()

        self.env = Environment(loader=PackageLoader('tghistory', 'templates'))

    def render(self, name, *args, **kwargs):
        """ render a template and then return it """
        if 'j2' not in name:
            name += '.j2'

        template = self.env.get_template(name)
        return template.render(*args, **kwargs)
