__author__ = 'ghoti'
import re
import Characters
import evelink.api
import evelink.corp
import sqlite3

#Returns a list to jabberbot of all poses under each(!) directors command (each corp)
#WARNING THIS IS SPAMMY IF YOU HAVE A LOT OF POSES JESUS FUCK
def towers(message):
    alltowers = ['Current POS states for all poses in each corp:  Data is cached and will not change for 30 minutes!']
    c = Characters.Characters()
    for toon in c.getall():
        #only try to get pos information IF a CORP api is provided, character api's do nothing here
        if toon.dirvcode:
            eve = evelink.eve.EVE()
            api = evelink.api.API(api_key=(toon.dirkeyid, toon.dirvcode))
            id = eve.character_id_from_name(toon.name)
            #char = evelink.char.Char(char_id=id, api=api)
            corp = evelink.corp.Corp(api=api)
            poses = corp.starbases()
            for pos in poses.result:
                conn = sqlite3.connect('static.db')
                c = conn.cursor()
                #this shit is ugly
                tower = c.execute('select typeName from invTypes where typeID={0}'.format(poses[0][pos]['type_id'])).fetchone()[0]
                moon = c.execute('select itemName from mapDenormalize where itemID={0}'.format(poses[0][pos]['moon_id'])).fetchone()[0]
                status = poses[0][pos]['state']
                try:
                    thispos = corp.starbase_details(poses[0][pos]['id'])
                    fuel = {}
                    for j in thispos.result['fuel']:
                        if j != 16275: #DONT GIVE A SHIT ABOUT STRONT
                            fuelname = c.execute('select typeName from invTypes where typeID={0}'.format(j)).fetchone()[0]
                            fuelamount = thispos.result['fuel'][j]
                #this might be the only case of error handling in this entire bot dear god im bad at this
                except evelink.api.APIError, e:
                    return 'API keys are fucked up, or :ccp:!'
                alltowers.append('{0} at {1} is {2} with {3} {4} remaining!'.format(tower, moon, status, fuelamount, fuelname))
    return alltowers

towers.rule='^!towers'