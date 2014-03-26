__author__ = 'ghoti'

import os
import ConfigParser
#This thingamabober holds basic info for each character we are pulling info from (ideally a dir from each corp)
class Characters():

    #def __init__(self, name, keyid, vcode, dirkeyid, dirvcode):
    #    self.name = name
    #    self.keyid = keyid
    #    self.vcode = vcode
    #    self.dirkeyid = dirkeyid
    #    self.dirvcode = dirvcode

    def __init__(self):
        #classception
        class Toon(object):
            def __init__(self, name, keyid, vcode, dirkeyid, dirvcode):
                self.name = name
                self.keyid = keyid
                self.vcode = vcode
                self.dirkeyid = dirkeyid
                self.dirvcode = dirvcode

        self.characters = []
        config = ConfigParser.ConfigParser()
        for file in os.listdir('config/characters/'):
            if file.endswith('.cfg'):
                config.readfp(open('config/characters/'+file))
                name = config.get('api', 'CharacterName')
                keyid = config.get('api', 'keyid')
                vcode = config.get('api', 'vcode')
                dirkeyid = config.get('api', 'dirkeyid')
                dirvcode = config.get('api', 'dirvcode')

                toonie = Toon(name, keyid, vcode, dirkeyid, dirvcode)
                self.characters.append(toonie)
    def getall(self):
        return self.characters