#
import os
import pytg
import logging
from pytg.exceptions import IllegalResponseException

from tghistory.lib.writer import Writer
from tghistory.lib.singleton import Singleton

LOG = logging.getLogger('tgh.lib.telegram')


class TelegramHistory(object, metaclass=Singleton):

    def __init__(self, args, config):
        self.args = args
        self.config = config

        if not os.path.exists(self.config.telegram.path):
            LOG.error('Cannot find telegram client! Path: %s'
                      % self.config.telegram.path)
            exit(-1)

        self.tg = pytg.Telegram(telegram=self.config.telegram.path,
                                pubkey_file=self.config.telegram.pubkey,
                                custom_cli_args=['--disable-colors'])
        self.send = self.tg.sender
        self.recv = self.tg.receiver

        # Other stuff we need
        self._me = None
        self._contacts = []

    def _contact_list(self, iter=False):
        """
        :param iter: yield the contact?
        """
        contact_list = self.send.contacts_list()
        for contact in contact_list:
            if contact.peer_type != 'user':
                continue

            self._contacts.append(contact)
            if iter:
                yield contact

        return self._contacts

    def _read_history_for_contact(self, contact):
        """ figure out the history for a given client """
        LOG.info('Reading history for {name}: peer id: {pid}, uid: {id}'.format(
            name=contact.print_name, pid=contact.peer_id, id=contact.id
        ))

        offset = 0
        count = self.config.telegram.batch_read_count
        while True:
            try:
                lines = self.send.history(contact.id, count, offset)
            except IllegalResponseException:
                break

            if not lines:
                break

            yield lines

            offset += count

    def run(self):
        """ run the main program """
        self._me = self.send.get_self()

        if self.args.contact:
            # resolve the contact
            pass

        for contact in self._contact_list(iter=True):
            # if we want to read from only a single client
            if self.args.contact and contact.username != self.args.contact:
                continue

            writer = Writer(me=self._me,
                            contact=contact,
                            args=self.args,
                            config=self.config)

            for lines in self._read_history_for_contact(contact):
                writer.write_lines(lines)
