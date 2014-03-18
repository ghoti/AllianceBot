__author__ = 'ghoti'


#This thingamabober holds basic info for each character we are pulling info from (ideally a dir from each corp)
class Characters():

    def __init__(self, name, keyid, vcode, dirkeyid, dirvcode):
        self.name = name
        self.keyid = keyid
        self.vcode = vcode
        self.dirkeyid = dirkeyid
        self.dirvcode = dirvcode