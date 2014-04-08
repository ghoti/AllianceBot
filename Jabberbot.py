__author__ = 'ghoti'
import os
import importer
import sleekxmpp
import time
import logging
import ConfigParser


import Notifications

class MUCBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick, roomsecret):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick
        self.roomsecret = roomsecret

        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open('config/jabber.cfg'))

        self.add_event_handler("session_start", self.start)

        self.add_event_handler("groupchat_message", self.muc_message)

        self.add_event_handler("muc::{0}::got_online".format(self.room), self.muc_online)

        self.n = Notifications.Notifications()

        self.botcommands = importer.Importer()

    def start(self, event):
        self.get_roster()
        self.send_presence()
        if self.roomsecret:
            self.plugin['xep_0045'].joinMUC(self.room, self.nick, password=self.roomsecret, wait=True)
        else:
            self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

        #for toon in self.n.characters:
        #    self.notificationrunner(toon)

        if self.config.get('jabber', 'notificationbot') == 'True':
            logging.info('STARTING NOTIFICATION RUNNER FOR LEADERSHIP')
            for toon in self.n.characters.getall():
                self.notificationrunner(toon)
        #self.schedule('notificationrunner', 1800, self.notificationrunner, repeat=True)


    def muc_message(self, msg):
        #if a command returns a list of items, send each list item individually, otherwise, just send the string
        for regex in self.botcommands.commands.keys():
           if regex.match(msg['body']):
            result = self.botcommands.commands[regex](msg['body'])
            if type(result).__name__ == 'list':
                for thing in result:
                    self.send_message(mto=msg['from'].bare,
                                      mbody=thing,
                                      mtype='groupchat')
            else:
                self.send_message(mto=msg['from'].bare,
                                  mbody=result,
                                  mtype='groupchat')

    def muc_online(self, presence):
        pass

    def notificationrunner(self, toon):
        messages = self.n.grabnotes(toon)
        self.schedule(toon.name, toon.apicachetime-time.time(), self.notificationrunner, args=(toon, ))
        logging.info('Queued {} to run notes in {}'.format(toon.name, toon.apicachetime-time.time()))
        msg=sleekxmpp.Message()
        msg['from'] = self.room + '/' + self.nick
        for message in messages:
            self.send_message(mto=msg['from'].bare,
                              mbody=message,
                              mtype='groupchat')
