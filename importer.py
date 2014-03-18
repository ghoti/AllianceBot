__author__ = 'ghoti'
import os, imp
from types import FunctionType
import re

#this is black magic
stripinternals = lambda x:x[0:2]!="__"

