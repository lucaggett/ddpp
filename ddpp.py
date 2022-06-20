"""
the main file for the ddpp.py library.
"""

# *-* coding: utf-8 *-*
# pylint: disable=line-too-long
from random import randrange, choice
from re import sub
from pprint import pprint
from os.path import abspath
from time import sleep
from ddpp_classes import Config
import json


class Monster_Manual:
    pass


class Instructions:
    """
    A class holding rolling instructions, which are used to generate random dice rolls
    """

    def __init__(self, instructions: str or [str], config=None):
        if not config:
            config = Config()
        self.instructions = (
            config.config_file[instructions]
            if instructions in config.config_file
            else instructions.split(" ")
            if isinstance(instructions, str)
            else instructions
            if isinstance(instructions, list)
            else None
        )
        # implementation for aliases
        # check for strings, split into array
        # if a list was passed, use it
        # if none of the above, pass None which will raise an error

        print(self.instructions)
        if instructions is None:
            raise TypeError("instructions must be a string or list")
        self.config = config
        self.__replace_variables()
        avg = 0
        for instruction in self.instructions:
            if instruction.startswith("+"):
                avg += int(instruction[1:]) / 2
            elif instruction.startswith("-"):
                avg += -int(instruction[1:]) / 2
            else:
                avg += self.__s_avg(
                    int(instruction.split("d")[0]), int(instruction.split("d")[1])
                )
        self.average = avg

    def __getitem__(self, item):
        """
        return the item at the index
        """
        return self.instructions[item]

    def __str__(self):
        return f"dice: {''.join(self.instructions)} | average: {self.average}"

    def __repr__(self):
        return f"dice: {''.join(self.instructions)} |  average: {self.average}"

    def __replace_variables(self):
        """
        replace variables in the instructions with their values from the config file
        """
        for idx, instruction in enumerate(self.instructions[:]):
            if instruction in self.config.variables:
                self.instructions[idx] = self.config.variables[self.instructions[idx]]

    def __iter__(self):
        """
        return a generator object that yields all individual rolls and absolute values
        """
        for instruction in self.instructions:
            if instruction.startswith("+"):
                yield int(instruction[1:]), instruction
            elif instruction.startswith("-"):
                yield -int(instruction[1:]), instruction
            else:
                num, die = instruction.split("d")
                yield self.s_roll(int(num), int(die))

    def __add__(self, other):
        """
        add two instructions together
        """
        if isinstance(other, Instructions):
            self.instructions.extend(other.instructions)
        elif isinstance(other, str):
            self.instructions.append(other)
        elif isinstance(other, int):
            self.instructions.append(f"+{other}")
        else:
            raise TypeError(f"unsupported type {type(other)}")
        return Instructions(self.instructions, self.config)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """
        subtract two instructions
        """
        if isinstance(other, int):
            self.instructions.append(f"-{other}")
        else:
            raise TypeError(f"unsupported type {type(other)}")

        return self

    def __isub__(self, other):
        return self.__sub__(other)

    def roll(self) -> tuple[int, str]:
        """
        roll out every individual instruction
        """
        out_num = 0
        out_str = ""
        for roll, justify in self.__iter__():
            out_num += roll
            out_str += justify + " "
        return out_num, out_str

    @staticmethod
    def __s_avg(number, die) -> int:
        """
        return the average roll for a single dice roll
        """
        return number * (die / 2)

    @staticmethod
    def s_roll(number: int, die: int) -> (int, str):  # Rolls an amount of the same dice
        """
        returns an int and a justification string
        generates a number based on amount of sides of the die and the number of dice
        """
        total = 0
        info = ""
        for _ in range(number):
            roll = randrange(1, die + 1)
            total += roll
            info += str(roll) + " + "
        return total, info[:-3]


def from_file(filepaths):
    """
    picks a value from each of a list of files,
    then returns a string made up of each of the choices.
    """
    filepaths = filepaths.split(" ")
    choices = []
    for file in filepaths:
        with open(file, "r", encoding="utf-8") as contentfile:
            choices.append(sub(r"(\n|\W)", "", choice(contentfile.readlines())))
    return " ".join(choices)


def initiative_tracker():
    """
    TODO: Finish this, it's currently broken and pretty useless
    """
    initiative_temp = {}
    active = True
    initiative = {}
    number = input("enter the number of entities in the initiative: ")
    for _ in range(0, int(number)):
        name = input("enter your entities Name")
        speed = input("enter the initiative of your Character")
        if speed == "roll":
            modifier = input("Enter your creature's initiative modifier")
            speed = str(Instructions.s_roll(1, 20)[0]) + modifier
        initiative.update({name: speed})
    print("beginning initiative")
    # noinspection PyTypeChecker
    initiative = dict(
        sorted(initiative.items(), key=lambda item: item[1], reverse=True)
    )
    initiative_temp.update(initiative)
    while active:
        initiative.update(initiative_temp)
        # noinspection PyTypeChecker
        initiative = dict(
            sorted(initiative.items(), key=lambda item: item[1], reverse=True)
        )
        for entity in initiative:
            print("Entity:", entity, "| Initiative:", initiative.get(entity))
            user_input = input()
            if user_input == "help":
                print(
                    "possible commands: add, remove, print, exit (press enter for next creature)"
                )
            if user_input == "add":
                name = input("enter the Name of your creature: ")
                speed = input("enter the initiative of your creature: ")
                initiative_temp.update({name: speed})
                # noinspection PyTypeChecker
                # initiative_temp = dict(sorted(initiative_temp.items(), key=lambda item: item[1], reverse=True))
            if user_input == "remove":
                to_remove = input("enter the Name of the creature you want to remove: ")
                print(to_remove)
                pprint(initiative_temp, width=1)
                if initiative_temp.pop(to_remove, -100) == -100:
                    print("entity not found")
                else:
                    pass
                    # print(f"{to_remove} will be removed at the start of the initiative")
            if user_input == "print":
                pprint(initiative, width=1)
            if user_input == "exit":
                active = False


def death_save():
    """
    creates an interactive prompt that helps your roll death saves
    """
    failures = 0  # initialise failures and successes to 0
    successes = 0
    adv = input("Do you have advantage on death saves? (yes/no)")
    while failures < 3 and successes < 3:
        input("Press Enter for your next death save")
        result = Instructions.s_roll(1, 20)
        if adv in ("yes", "yup"):
            advroll = Instructions.s_roll(1, 20)
            oldroll = result
            if advroll > result:
                result = advroll
            print("You rolled " + str(oldroll) + " and " + str(advroll))
        else:
            print("You rolled " + str(result))
        if result < 10:
            failures += 1
        else:
            successes += 1
        print(f"Successes: {successes} | Failures: {failures}")
    if successes == 3:
        print("You are stable")
    if failures == 3:
        print("You are dead")


def generate_heist():
    """
    generates a heist
    """
    print("Booting Heist-a-Tron 3000")
    sleep(1)
    print("Loading...")
    sleep(1)
    loc_mod = [
        "Tiny",
        "Alien",
        "Crowded",
        "Hazardous",
        "Dimly Lit",
        "Spooky",
        "Heavily Fortified",
        "Hi-Tech",
        "Night-time",
        "Haunted",
        "Abandoned",
        "Underwater",
        "Famous",
        "Russian",
        "Misty",
        "Quiet",
        "Cosy",
        "Dystopian",
        "Heavy-metal",
        "Gothic",
    ]
    loc = [
        "Art gallery",
        "Spaceship",
        "Race track",
        "Nuclear Power Plant",
        "Airport",
        "Marketplace",
        "Forest campsite",
        "Office block",
        "Beach resort",
        "Casino",
        "Castle",
        "Bunker",
        "British country house",
        "School fete",
        "Museum",
        "Factory",
        "Farm",
        "Music festival",
        "Shopping centre",
        "Mountain lodge",
    ]
    sec = [
        "A 3D laser grid",
        "Guards armed with AK47s",
        "An underground one-way vault",
        "Sleeping nerve agents",
        "A horde of killer bees",
        "Lots of cameras",
        "Ghosts",
        "Trap rooms",
        "Bear detectors",
        "Biometric scanners",
        "Murderous AI",
        "A time sensitive lock",
        "A literal honeytrap",
        "Secret squad of ninjas",
        "Moat",
        "Turrets",
        "Silent alarms",
        "A password longer than 20 characters",
        "Snipers",
        "Roll three times instead of 2",
    ]
    prize = [
        "A secret formula to genetically modified honey that is the most delicious thing in the world",
        "A crown decorated with diamond and topaz bees",
        "Nicolas Cage",
        "The unseen extended cut of the Bee Movie",
        "Moonlight honey, the rarest of honeys, harvested from the top of Mt",
        "The 1954 Medal for the European Spelling Bee, made out of pure gold",
        "A bee in perspex, a famous piece by Damien Hirst",
        "Spooky honey, one of the rarest specimens of honey from the nectar of the Ghost Orchid",
    ]
    organizers = [
        "A group of bees",
        "Secretly a bear",
        "A typical villainous boss type",
        "Running this as a front for illegal weapons",
        "Has a keen eye for fine headwear",
        "Is a prince of a foreign land",
        "Doesn’t take no for an answer",
        "A movie director looking for his next superstar",
        "A multi-millionaire",
        "A radical wildlife conservationist",
        "A cult leader obsessed with the coming of thebees",
    ]
    twist = [
        "It was all a gameshow!",
        "Animal poachers are waiting at the exit!",
        "Dr. Doolittle was tailing them this whole time! ",
        "The exit is surrounded by sharks!",
        "The only way out is by flying a helicopter!",
        "One of the bears was a human in disguise!",
        "The bees are actually drones!",
        "The honey is spiked with hallucinogens!",
        "The prize has a hidden explosive!",
        "It was all a test set up by the head crime bear, Marcus Anetonne",
    ]
    with open("heist.txt", "w", encoding="utf-8") as file:
        file.write("Location: " + choice(loc_mod) + " " + choice(loc) + "\n")
        file.write("Security: " + choice(sec) + " and " + choice(sec) + "\n")
        file.write("Prize: " + choice(prize) + "\n")
        file.write("Organizer: " + choice(organizers) + "\n")
        file.write("Twist: " + choice(twist) + "\n")
    with open("heist.txt", "r", encoding="utf-8") as file:
        print("\n" + file.read())
        print("\n" + "Heist has been written to " + abspath("heist.txt"))


def generate_bear(weakness=False):
    """
    generates a bear
    """
    print("Booting Bear-a-Tron 3000")
    sleep(1)
    personalites = [
        "Shrewd",
        "Vicious",
        "Risk taking",
        "Greedy",
        "Vengeful",
        "Impulsive",
        "Patient",
        "Kind",
        "Careful",
        "Dopey",
        "Sly",
        "Wacky",
    ]
    roles = [
        "The Thug",
        "The Big Talker",
        "The Pickpocket",
        "The Designated Driver",
        "The Tech Guy",
        "The Mastermind",
        "The Seductor",
        "The Demolition Expert",
        "The Locksmith",
        "The Scout",
    ]
    bears = [
        "Grizzly Bear (Mauling)",
        "Polar Bear (Anything to do with fish)",
        "Panda Bear (Kung Fu)",
        "Black Bear (Scavenging)",
        "Sun Bear (Sneaking)",
        "Honey badger (Absolute chaos)",
        "Koala (Convincing)",
        "Red Panda (Acrobatics)",
        "Spectacled Bear (Spotting things)",
        "Goose (Honking)",
    ]
    weaknesses = [
        "Has a honey addiction",
        "Deeply mistrusts bears",
        "Is out of shape",
        "Only speaks one word sentences in English",
        "Has never done anything criminal",
        "Is wildly incompetent at fine motor control",
        "Is scared of bees",
        "Is allergic to honey",
    ]
    print(
        "Your bear is a "
        + choice(bears)
        + " with a "
        + choice(personalites)
        + " personality."
    )
    print("They're " + choice(roles) + " in this heist")
    if weakness:
        print("They have a weakness: " + choice(weaknesses))
