__author__ = 'ghoti'
import ConfigParser
import sys

import Notifications
import Characters
import Notifications
import Jabberbot
import logging

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

def main():
    config = ConfigParser.ConfigParser()
    config.readfp(open('config/jabber.cfg'))
    name = config.get('jabber', 'name')
    server = config.get('jabber', 'server')
    conference = config.get('jabber', 'conference')
    room = config.get('jabber', 'room')
    password = config.get('jabber', 'password')
    roomsecret = config.get('jabber', 'roomsecret')

    logging.basicConfig(level=logging.DEBUG, format=('%(levelname)-8s %(message)s'))

    if roomsecret == '':
        xmpp = Jabberbot.MUCBot(server, password, room+'@'+conference, name, roomsecret=None)
    else:
        xmpp = Jabberbot.MUCBot(server, password, room+'@'+conference, name, roomsecret)
    xmpp.register_plugin('xep_0030') #service discovery
    xmpp.register_plugin('xep_0045') #MUC
    xmpp.register_plugin('xep_0199') #ping

    if xmpp.connect():

        xmpp.process(block=True)

        print('Done')
    else:
        print('Unable to Connect')

if __name__ == '__main__':
    main()