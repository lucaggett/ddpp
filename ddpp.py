"""
the main file for the ddpp.py library.
"""

# *-* coding: utf-8 *-*
# pylint: disable=line-too-long
import os.path
import random
import re
import pprint
import time


def s_roll(number, die):  # Rolls an amount of the same dice
    """
    returns an int
    generates a random number based on amount of sides of the die and the number of dice
    """
    total = 0
    info = ""
    for _ in range(number):
        roll = random.randrange(1, die) + 1
        total += roll
        info += str(roll) + " + "
    return total, info[:-3]


def mult_roll(instructions):  # Rolls arbitrary Combinations of dice
    """
    returns 2 variables: total (an integer) and rolls (a string)

    returns a number and a string, based on rolls and modifiers parsed from instructions

    instructions may either be a string or a list
    """
    if type(instructions) == str:
        instructions = instructions.split(" ")
    total = 0  # Running total
    rolls = ""  # Justification
    for instruction in instructions:
        if instruction.find("+") >= 0:  # Positive Modifier
            numbers = re.sub(r"\D", "", instruction)
            total += int(numbers)
            rolls += str(numbers) + " + "
        elif instruction.find("-") >= 0:  # Negative Modifier
            numbers = re.sub(r"\D", "", instruction)
            total -= int(numbers)
            rolls += str(numbers) + " + "
        elif instruction.find("d") > 0:  # Dice Roll
            args = instruction.split("d")
            result, info = s_roll(int(args[0]), int(args[1]))
            total += result
            rolls += info + " + "
        else:  # Invalid Input
            pass
    return total, rolls[:-3]


def replace_variables(instructions, variables):
    """
    Replaces variables in instructions by concrete values

    returns sanitized input, an instruction set which mult_roll can accept

    replaces variables with numbers parsed from a .config file and recreates the output
    """
    sanitized = []
    for instruction in instructions:
        instruction_positive = True
        variable_positive = True
        if instruction.find("[") >= 0:  # If is variable
            if instruction.find("-") >= 0:  # If instruction is subtractive
                instruction_positive = False
            variable_name = re.sub(r"[^A-Za-z]", "", instruction)
            variable = str(variables.get(variable_name))
            if variable.find("-"):  # If value of variable is negative
                variable_positive = False
            variable = re.sub(r"\D", "", variable)
            if (
                variable_positive == instruction_positive
            ):  # If ++ or -- (thus + in total)
                sanitized.append("+" + str(variable))
            else:  # If +- or -+ (thus - in total)
                sanitized.append("+" + str(variable))
        else:  # If no instruction
            sanitized.append(instruction)
    return sanitized


def roll_from_list(name, config):
    """
    Rolls predefined roll from variables.ddpp and config.ddpp
    """
    return mult_roll(replace_variables(dict.get(name), config.variables))


def roll_from_string(inputt, config):
    """
    rolls from any string, replacing present variables if they are present.
    """
    inputs = inputt.split(" ")
    return mult_roll(replace_variables(inputs, config.variables))


def s_avg(number, die):
    """
    Returns the average value of an amount of the same die
    """
    return number * ((1 + die) / 2)


def mult_avg(instructions):
    """
    Returns the average of an arbitrary roll
    """
    total = 0
    for instruction in instructions:
        if instruction.find("+") >= 0:
            numbers = re.sub(r"\D", "", instruction)
            total += int(numbers)
        elif instruction.find("-") >= 0:
            numbers = re.sub(r"\D", "", instruction)
            total -= int(numbers)
        elif instruction.find("d") > 0:
            args = instruction.split("d")
            result = s_avg(int(args[0]), int(args[1]))
            total += result
        else:
            print("invalid")
    return total


def avg_from_list(name, config):
    """
    Returns the average of a list of rolls.
    Supports variables and raw addition
    """
    return mult_avg(replace_variables(config.config_file.get(name), config.variables))


def avg_from_string(data, var):
    """
    returns the average of a string of rolls
    supports variables and raw addition
    """

    inputs = data.split(" ")
    return mult_avg(replace_variables(inputs, var))


def random_from_file(filepaths):
    """
    picks a random value from each of a list of files,
    then returns a string made up of each of the choices.
    """
    filepaths = filepaths.split(" ")
    choices = []
    for file in filepaths:
        with open(file, "r", encoding="utf-8") as contentfile:
            choices.append(
                re.sub(r"(\n|\W)", "", random.choice(contentfile.readlines()))
            )
    return " ".join(choices)


def initiative_tracker():
    """
    Starts an initiative tracker, initialised as an empty combat.
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
            speed, justify = str(s_roll(1, 20)) + modifier
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
                pprint.pprint(initiative_temp, width=1)
                if initiative_temp.pop(to_remove, -100) == -100:
                    print("entity not found")
                else:
                    pass
                    # print(f"{to_remove} will be removed at the start of the initiative")
            if user_input == "print":
                pprint.pprint(initiative, width=1)
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
        result = s_roll(1, 20)
        if adv in ("yes", "yup"):
            advroll = s_roll(1, 20)
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
    time.sleep(1)
    print("Loading...")
    time.sleep(1)
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
    with open("heist.txt", "w") as f:
        f.write("Location: " + random.choice(loc_mod) + " " + random.choice(loc) + "\n")
        f.write("Security: " + random.choice(sec) + " and " + random.choice(sec) + "\n")
        f.write("Prize: " + random.choice(prize) + "\n")
        f.write("Organizer: " + random.choice(organizers) + "\n")
        f.write("Twist: " + random.choice(twist) + "\n")
    with open("heist.txt", "r") as f:
        print("\n" + f.read())
        print("\n" + "Heist has been written to " + os.path.abspath("heist.txt"))


def generate_bear(weakness=False):
    """
    generates a bear
    """
    print("Booting Bear-a-Tron 3000")
    time.sleep(1)
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
        + random.choice(bears)
        + " with a "
        + random.choice(personalites)
        + " personality."
    )
    print("They're " + random.choice(roles) + " in this heist")
    if weakness:
        print("They have a weakness: " + random.choice(weaknesses))
