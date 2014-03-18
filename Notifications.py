__author__ = 'ghoti'

import os
import ConfigParser
import datetime
import sqlite3
import evelink.api
import evelink.char
import evelink.eve
import evelink.corp

import Characters

#This here class will handle all our notification grabbing and processing
class Notifications():

    def __init__(self):
        config = ConfigParser.ConfigParser()
        self.characters = []
        for file in os.listdir('config/characters/'):
            if file.endswith('.cfg'):
                config.readfp(open('config/characters/'+file))
                name = config.get('api', 'CharacterName')
                keyid = config.get('api', 'keyid')
                vcode = config.get('api', 'vcode')
                dirkeyid = config.get('api', 'dirkeyid')
                dirvcode = config.get('api', 'dirvcode')

                toonie = Characters.Characters(name, keyid, vcode, dirkeyid, dirvcode)
                self.characters.append(toonie)
        self.conn = sqlite3.connect('static.db')
        self.c = self.conn.cursor()

    def noteid(self):
        return{
            16:self.application,
            17:self.denial,
            18:self.acceptance,
            45:self.anchoralert,
            46:self.vulnstruct,
            47:self.invulnstruct,
            48:self.sbualert,
            76:self.posfuel,
            86:self.tcualert,
            87:self.sbushot,
            88:self.ihubalert,
            93:self.pocoalert,
            94:self.pocorf,
            96:self.fwwarn,
            97:self.fwkick,
            111:self.bounty,  #TURNS OUT THIS IS SPAMMY AS FUCK DAMN YOU WATCH YOSELF
            128:self.joinfweddit #join note is same as app note with different id hue
        }

    def bounty(self, id, toon):
        bounty = self.gettext(id, toon)
        name = self.getname(bounty[id]['victimID'])
        return 'A bounty on {0} was claimed!'.format(name[0])

    def application(self, id, toon):
        app = self.gettext(id, toon)
        name = self.getname(app[id]['charID'])
        text = app[id]['applicationText'].strip()
        #corp = app[id]['corporationName']
        corp = self.getcorp(toon, app[id]['corpID'])
        if text:
            return '{0} has apped to {1}: {2}'.format(name[0],corp, text)
        else:
            return '{0} has apped to {1}'.format(name[0], corp)
    def denial(self, id, toon):
        app = self.gettext(id, toon)
        name = self.getname(app[id]['charID'])
        return '{0} was denied into fweddit!'.format(name[0])
    def acceptance(self, id, toon):
        return 'Someone was accepted into fweddit!'
    def anchoralert(self, id, toon):
        anchor = self.gettext(id, toon)
        moon = self.c.execute('select itemName from mapDenormalize where itemID={0}'.format(anchor[id]['moonID']))
        moon = moon.fetchone()[0]
        thing = self.c.execute('select typeName from invTypes where typeID={0}'.format(anchor[id]['typeID']))
        thing = thing.fetchone()[0]
        who = self.getcorp(toon, anchor[id]['corpID'])
        return '{0} was anchored on {1} by {2}!'.format(thing, moon, who)
    def vulnstruct(self, id, toon):
        return 'Something went vulnerable in our sov!'
    def invulnstruct(self, id, toon):
        return 'Something went invulnerable in our sov!'
    def sbualert(self, id, toon):
        return 'Someone anchored an SBU in our sov!'
    def posfuel(self, id, toon):
        #I HAS NO IDEA WHAT INFO IS USEFUL HERE
        pos = self.gettext(id, toon)
        moon = self.c.execute('select itemName from mapDenormalize where itemID={0}'.format(pos[id]['moonID']))
        moon = moon.fetchone()[0]
        return 'THE TOWER AT %s NEEDS FUELS PLS - %d remaining' % (moon, pos[id]['- quantity'])
    def tcualert(self, id, toon):
        return 'Someone shot a TCU we own!'
    def sbushot(self, id, toon):
        return 'Someone shot an SBU we own!'
    def ihubalert(self, id, toon):
        return 'Someone shot an IHUB we own!'
    def pocoalert(self, id, toon):
        return 'Someone shot a POCO we own!'
    def pocorf(self, id, toon):
        return 'Someone reinforced a POCO we own!'
    def fwwarn(self, id, toon):
        return 'We are in danger of being kicked from FW!'
    def fwkick(self, id, toon):
        return 'We have been kicked from FW! RIP!'
    def joinfweddit(self, id, toon):
        app = self.gettext(id, toon)
        name = self.getname(app[id]['charID'])
        corp = self.getcorp(toon, app[id]['corpID'])
        return '{0} has joined {1}!'.format(name[0], corp)

    def gettext(self,notificationid, toon):
        api = evelink.api.API(api_key=(toon.keyid, toon.vcode))
        eve = evelink.eve.EVE()
        id = eve.character_id_from_name(toon.name)
        char = evelink.char.Char(char_id=id, api=api)

        notes = char.notification_texts(notification_ids=(notificationid))
        return notes[0]

    def getname(self, eveid):
        eve = evelink.eve.EVE()
        return eve.character_name_from_id(eveid)

    def getcorp(self, toon, corpid):
        api = evelink.api.API(api_key=(toon.keyid, toon.vcode))
        corp = evelink.corp.Corp(api=api)
        return corp.corporation_sheet(corpid)[0]['name']


    def grabnotes(self):

        eve = evelink.eve.EVE()
        for toon in self.characters:
            api = evelink.api.API(api_key=(toon.keyid, toon.vcode))
            id = eve.character_id_from_name(toon.name)
            char = evelink.char.Char(char_id=id, api=api)

            notes = char.notifications()
            messages = []

            for notificationID in notes[0]:
                now = datetime.datetime.now()

                timesent = notes[0][notificationID]['timestamp']
                #timesent = datetime.datetime.strptime(timesent,'%Y-%m-%d %H:%M:%S')
                timesent = datetime.datetime.fromtimestamp(timesent)
                #print timesent, now-datetime.timedelta(minutes=60)
                if timesent > now-datetime.timedelta(days=1):
                    sendme = self.noteid().get(notes[0][notificationID]['type_id'], '')
                    if sendme:
                        message = sendme(notificationID, toon)
                        self.lastnotification = message
                        #self.send_message(mto=mess['from'].bare, mbody=message, mtype='groupchat')
                        messages.append(message)
            return messages


