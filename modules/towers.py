__author__ = 'ghoti'
import re
import Characters
import evelink.api
import evelink.corp
import sqlite3

def towers(message):
    alltowers = []
    c = Characters.Characters()
    for toon in c.getall():
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
                except evelink.api.APIError, e:
                    print e
                #print tower + 'at' + moon + 'is' + status + 'with' + fuelamount + fuelname + 'remaining'
                alltowers.append('{0} at {1} is {2} with {3} {4} remaining!'.format(tower, moon, status, fuelamount, fuelname))
    return alltowers

towers.rule='^!towers'