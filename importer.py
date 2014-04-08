__author__ = 'ghoti'
import os, imp
from types import FunctionType
import re
import ConfigParser
import logging

#this is black magic
stripinternals = lambda x:x[0:2]!="__"

class Importer():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open('config/jabber.cfg'))
        self.blacklist = config.get('jabber', 'blacklist')
        self.commands = {}
        for file in os.listdir('modules/'):
            if file.endswith('.py'):
                if not self.blacklist.count(file.strip('.py')):
                    logging.info('Importing module {}'.format(file))
                    self._import(file)

    def _import(self, file):
        mod = imp.load_source(file.split(".")[0], "modules/"+file)
        d = dir(mod)
        d = filter(stripinternals, d)
        for item in d:
            member = getattr(mod, item)
            if not isinstance(member, FunctionType):
                next
            list = dir(member)
            list =  filter(stripinternals, list)
            if "rule" in list:
                rule = getattr(member, "rule")
                rule = re.compile(rule)
                self.commands[rule] = member