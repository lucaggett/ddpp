"""
This is a command line interface for ddpp.py.
"""

import argparse
import os
import sys
import time

import ddpp

parser = argparse.ArgumentParser(description='DDPP interface, use -h for help')
parser.add_argument('-r', '--roll', help='roll a die, input is in format XdY')
parser.add_argument('-a', '--alias', help='use an alias, input is the name of an alias. '
                                          'requires a config file to be imported, use the -c flag')
parser.add_argument('-c', '--config', help='import a config file, input is the path to the file')
parser.add_argument('-l', '--list', help='list all aliases')
parser.add_argument('-s', '--stats', help='show stats, requires character file as input')
parser.add_argument('--create', help='create a new character', nargs=True)
args = parser.parse_args()

print(args)
print(dir(args))

if args.roll:
    print(ddpp.mult_roll(args.roll))