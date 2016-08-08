#
import os
import time
import pytg
import arrow
import logging
from pytg.exceptions import IllegalResponseException, NoResponse

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

    def _chat_list(self, iter=False):
        """
        :param iter: yield the contact?
        """

        def invalid_user(user):
            """ skip this user? """
            if hasattr(user, 'username'):
                if ('Bot' in user.username or
                    '_bot' in user.username or
                        '_Bot' in user.username):
                    return True
            return False

        # go through the open chats. not all/any are
        # could actually be contacts
        chat_list = self.send.dialog_list()
        for chat in chat_list:
            if chat.peer_type != 'user':
                continue

            if invalid_user(chat):
                continue

            self._contacts.append(chat)
            if iter:
                yield chat

        # and go through the contacts list
        # but skip any users that have already been included
        contact_list = self.send.contacts_list()
        for contact in contact_list:
            if contact.peer_type != 'user':
                continue

            if contact in self._contacts:
                continue

            if invalid_user(contact):
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
        retries = 0
        lines_day = []
        yield_lines = []
        count = self.config.telegram.batch_read_count

        while True:
            try:
                retr_lines = self.send.history(contact.id, count, offset)
            except NoResponse:
                retries += 1
                if retries == 5:
                    break

                LOG.info('No response, sleeping for 60 seconds')
                time.sleep(60)
                continue
            except IllegalResponseException:
                break

            if not retr_lines:
                break

            # keep track until we're not on a different day
            for line in retr_lines:
                dt = arrow.get(line.date).to(self.config.general.timezone)
                dt = dt.format('YYYYMMDD')

                # it's a new day
                if dt != lines_day:

                    LOG.debug('new day: %i lines, %s' % (len(yield_lines), dt))

                    if yield_lines:
                        yield yield_lines
                        yield_lines = []

                    lines_day = dt

                # add this line now to the current day
                yield_lines.append(line)

            offset += count
            time.sleep(5)

    def run(self):
        """ run the main program """
        self._me = self.send.get_self()

        # get the ID
        if self.args.contact:
            c = self.args.contact
            if c[0] != '@': c = '@' + c
            c = self.send.user_info(c)

        for contact in self._chat_list(iter=True):
            # if we want to read from only a single client
            if self.args.contact and contact.id != c.id:
                continue

            writer = Writer(me=self._me,
                            contact=contact,
                            args=self.args,
                            config=self.config)

            for lines in self._read_history_for_contact(contact):
                writer.write_lines(lines)
