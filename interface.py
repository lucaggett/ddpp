"""
This is a command line interface for ddpp.py.
"""

import argparse
import os
import sys
import time

import ddpp
import ddpp_classes

parser = argparse.ArgumentParser(description="DDPP interface, use -h for help")
parser.add_argument("-r", "--roll", help="roll a die, input is in format XdY +Z")
parser.add_argument(
    "-a",
    "--alias",
    help="use an alias, input is the name of an alias. "
    "uses aliases from config.ddpp by default, use --no-default to specify a custom file",
)
parser.add_argument(
    "--config",
    help="edit the config files, optionally takes a filepath to a custom config file",
    nargs="?",
    default="",
    const="config/config.ddpp",
)
parser.add_argument(
    "-l",
    "--list",
    help="list all currently loaded shortcuts and variables",
    action="store_true",
)
parser.add_argument(
    "-nd",
    "--no-default",
    help="flag to disable the import of the default config files",
    action="store_true",
)
parser.add_argument(
    "-s",
    "--stats",
    help="show stats, requires character file as input",
    metavar="FILEPATH",
)
parser.add_argument("--bear", help="generate a random bear", action="store_true")
parser.add_argument(
    "--hat",
    help="generate a random hat. enter a series and a tier",
    nargs=2,
    metavar=("SERIES", "TIER"),
)
parser.add_argument(
    "-v",
    "--verbose",
    help="outputs additional information about the things ddpp is doing",
    action="store_true",
)
parser.add_argument(
    "--heist", help="generate a random heist, writes to heist.txt", action="store_true"
)

args = parser.parse_args()
c = ddpp_classes.Config()

if not args.no_default:
    if os.path.exists("config/config.ddpp"):
        if args.verbose:
            print("Found config file, importing config.ddpp")
        c.import_config()
    if os.path.exists("config/variables.ddpp"):
        if args.verbose:
            print("Found variables file, importing variables.ddpp")
        c.import_variables()
if args.roll:
    res = ddpp.mult_roll(args.roll)
    print("You rolled:", res[0])
    print("Rolls:", res[1])

if args.bear:
    ddpp.generate_bear()

if args.heist:
    ddpp.generate_heist()

if args.stats:
    imp = ddpp_classes.Character()
    imp.import_char(args.stats)

if args.list:
    print("Shortcuts:")
    for s, m in c.config_file.items():
        print("\t", s, ":", m)
    print("Variables:")
    for v, n in c.variables.items():
        print("\t", v, ":", n)

if args.alias:
    if args.alias in c.config_file:
        res, rolls = ddpp.mult_roll(c.config_file[args.alias])
        print("result is: " + str(res))
        print("you rolled: " + str(rolls))

if args.config:
    ACTIVE = True
    print("Welcome to the interactive configuration editor for ddpp!")
    print("Type 'exit' to quit.")
    print("Type 'help' for help.\n")
    while ACTIVE:
        cmd = input(">> ")
        if cmd == "exit":
            ACTIVE = False
        elif cmd == "help":
            print("Commands:")
            print("\t'exit' - quit the editor")
            print("\t'list' - list all shortcuts and variables")
            print("\t'addvar' - create a variable")
            print("\t'rmvar' - remove a variable")
            print("\t'rmshortcut' - remove a shortcut")
            print("\t'addshortcut' - create a shortcut")
        elif cmd == "list":
            print("Shortcuts:")
            for s, m in c.config_file.items():
                print("\t", s, ":", m)
            print("Variables:")
            for v, n in c.variables.items():
                print("\t", v, ":", n)
        elif cmd == "addvar":
            c.create_variable()
        elif cmd == "rmvar":
            c.delete_variable()
        elif cmd == "rmshortcut":
            c.delete_config()
        elif cmd == "addshortcut":
            c.create_config()
        else:
            print("Unknown command")
