"""
This is a command line interface for ddpp.py.
"""

import argparse
import os
import platform
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
    "--character",
    help="create or load a character, optionally takes the filepath to a character file",
    nargs="?",
    default=False,
    const=True,
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
parser.add_argument("--bear", help="generate a random bear", action="store_true")
parser.add_argument(
    "--hat", help="generate a random hat. enter a series and a tier", nargs=2
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
config_object = ddpp_classes.Config()

if not args.no_default:
    if os.path.exists("config/config.ddpp"):
        if args.verbose:
            print("Found config file, importing config.ddpp")
        config_object.import_config()
    if os.path.exists("config/variables.ddpp"):
        if args.verbose:
            print("Found variables file, importing variables.ddpp")
        config_object.import_variables()
if args.roll:
    # print(ddpp.replace_variables(args.roll, c.variables))
    res = ddpp.mult_roll(ddpp.replace_variables(args.roll, config_object.variables))
    print("You rolled:", res[0])
    print("Rolls:", res[1])

elif args.bear:
    ddpp.generate_bear()

elif args.heist:
    ddpp.generate_heist()

elif args.list:
    print("Shortcuts:")
    for s, m in config_object.config_file.items():
        print("\t", s, ":", m)
    print("Variables:")
    for v, n in config_object.variables.items():
        print("\t", v, ":", n)

elif args.alias:
    if args.alias in config_object.config_file:
        res, rolls = ddpp.Instructions(config_object.config_file[args.alias], config_object).roll()
        print("result is: " + str(res))
        print("you rolled: " + str(rolls))

elif args.config:
    ACTIVE = True
    print(
        f"Welcome to the interactive configuration editor for ddpp!\nRunning on "
        f"{platform.system()} {platform.release()} ({platform.architecture()[0]} {platform.machine()})"
    )
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
            print("\t'mkvar' - create a variable")
            print("\t'rmvar' - remove a variable")
            print("\t'rmsc' - remove a shortcut")
            print("\t'mksc' - create a shortcut")
        elif cmd == "list":
            print("Shortcuts:")
            for s, m in config_object.config_file.items():
                print("\t", s, ":", m)
            print("Variables:")
            for v, n in config_object.variables.items():
                print("\t", v, ":", n)
        elif cmd == "mkvar":
            config_object.create_variable()
        elif cmd == "rmvar":
            config_object.delete_variable()
        elif cmd == "rmsc":
            config_object.delete_config()
        elif cmd == "mksc":
            config_object.create_config()
        else:
            print("Unknown command")
else:
    print("No arguments given, use -h for help.")
