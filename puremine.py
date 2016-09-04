#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the new base initialization layer for Puremine.
# Always call this instead of server_core/core.py

from server_core.core import main


def str2bool(string):
    trues = ('True', 'true')
    falses = ('False', 'false')
    if string in trues:
        return True
    elif string in falses:
        return False
    else:
        raise TypeError("String %s isn't a boolean!" % string)


properties = {}  # Dict for configuration
try:
    with open('server.properties') as config:
        for line in config.readlines():
            if not line.startswith("#"):  # If line isn't a comment
                key, value = line.strip().split('=')  # Split key and value
                if value != "":  # If value isn't empty
                    if value in ('True', 'false', 'true', 'False'):  # If line is a boolean
                        properties[key] = str2bool(value)  # Add key and value to our dictionary
                        continue
                    elif value.isdigit():  # If line is a number
                        properties[key] = int(value)
                        continue
                    else:
                        properties[key] = value
except IOError:
    print("Config file don't found, using defaults...")
main(properties)
