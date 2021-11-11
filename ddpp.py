"""
the main file for the ddpp.py library.
"""

# *-* coding: utf-8 *-*
# pylint: disable=line-too-long

import random
import re
import pprint


def s_roll(number, die):  # Rolls an amount of the same dice
    """
    returns an int
    generates a random number based on amount of sides of the die and the number of dice
    """
    total = 0
    for _ in range(number):
        roll = random.randrange(1, die)+1
        total += roll
    return total


def mult_roll(instructions):  # Rolls arbitrary Combinations of dice
    """
    returns 2 variables: total (an integer) and rolls (a string)

    returns a number and a string, based on rolls and modifiers parsed from instructions

    instructions may either be a string or a list
    """

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
            result = s_roll(int(args[0]), int(args[1]))
            total += result
            rolls += str(result) + " + "
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
            if variable_positive == instruction_positive:  # If ++ or -- (thus + in total)
                sanitized.append("+" + str(variable))
            else:  # If +- or -+ (thus - in total)
                sanitized.append("+" + str(variable))
        else:  # If no instruction
            sanitized.append(instruction)
    return sanitized


def roll_from_list(name, config):
    """
    Rolls predefined roll from variables.ddpp or config.ddpp
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
    return mult_avg(replace_variables(config.configFile.get(name), config.variables))



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
        with open(file, "r") as contentfile:
            choices.append(re.sub(r"(\n|\W)", "", random.choice(contentfile.readlines())))
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
        speed = input("enter the initiative of your character")
        if speed == "roll":
            modifier = input("Enter your creature's initiative modifier")
            speed = s_roll(1, 20)+int(modifier)
        initiative.update({name: speed})
    print("beginning initiative")
    # noinspection PyTypeChecker
    initiative = dict(sorted(initiative.items(), key=lambda item: item[1], reverse=True))
    initiative_temp.update(initiative)
    while active:
        initiative.update(initiative_temp)
        # noinspection PyTypeChecker
        initiative = dict(sorted(initiative.items(), key=lambda item: item[1], reverse=True))
        for entity in initiative:
            print("Entity:", entity, "| Initiative:", initiative.get(entity))
            user_input = input()
            if user_input == "help":
                print("possible commands: add, remove, print, exit (press enter for next creature)")
            if user_input == "add":
                name = input("enter the Name of your creature: ")
                speed = input("enter the initiative of your creature: ")
                initiative_temp.update({name: speed})
                # noinspection PyTypeChecker
                initiative_temp = dict(sorted(initiative_temp.items(),
                                              key=lambda item: item[1],
                                              reverse=True))
            if user_input == "remove":
                to_remove = input("enter the Name of the creature you want to remove: ")
                print(to_remove)
                pprint.pprint(initiative_temp, width=1)
                if initiative_temp.pop(to_remove, -100) == -100:
                    print("entity not found")
                else:
                    print(f"{to_remove} will be removed at the start of the initiative")
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
