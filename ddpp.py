import random
import re
import timeit
from typing import Dict, Any


class ddpp():  # Saves Required Data (config dicts)
    def __init__(self):
        self.config = {}
        self.i = 0
        self.variables = {}

    def importddpp(self):
        # Import all config files into dictionaries

        with open("config.ddpp") as config:
            for line in config:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1:len(line_tok)]}
                self.config.update(localdict)
                self.i += 1

        with open("character.var") as character:
            for stat in character:
                stat = stat.replace("\n", "")
                stat = stat.split(" ")
                localstat = {stat[0]: stat[1]}
                self.variables.update(localstat)

        with open("custom.var") as custom:
            for variable in custom:
                var = var.replace("\n", "")
                var = var.split(" ")
                localvar = {var[0]: var[1]}
                self.variables.update(localvar)


def s_roll(number, die):  # Rolls an amount of the same dice
    total = 0
    for i in range(0, number):
        roll = random.randrange(1, die, 1)
        total += roll
    return total


def mult_roll(instructions):  # Rolls arbitrary Combinations of dice
    total = 0  # Running total
    rolls = ""  # Justification
    for instruction in instructions:
        if instruction.find("+") >= 0:  # Positive Modifier
            numbers = re.sub("\D", "", instruction)
            total += int(numbers)
            rolls += str(numbers) + " + "
        elif instruction.find("-") >= 0:  # Negative Modifier
            numbers = re.sub("\D", "", instruction)
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


def replace_variables(instructions, variables):  # Replaces variables in instructions by concrete values
    sanitized = []
    for instruction in instructions:
        instruction_positive = True
        variable_positive = True
        if instruction.find("[") >= 0:  # If is variable
            if instruction.find("-") >= 0:  # If instruction is subtractive
                instruction_positive = False
            variable_name = re.sub("[^A-Za-z]", "", instruction)
            variable = str(variables.get(variable_name))
            if variable.find("-"):  # If value of variable is negative
                variable_positive = False
            variable = re.sub("\D", "", variable)
            if variable_positive == instruction_positive:  # If ++ or -- (thus + in total)
                sanitized.append("+" + str(variable))
            else:  # If +- or -+ (thus - in total)
                sanitized.append("+" + str(variable))
        else:  # If no instruction
            sanitized.append(instruction)
    return sanitized


def roll_from_list(name, dict, var):  # Rolls a roll defined in the config
    return mult_roll(replace_variables(dict.get(name), var))


def roll_from_string(input, var):  # Rolls Rol defined in String
    inputs = input.split(" ")
    return mult_roll(replace_variables(inputs, var))


def s_avg(number, die):  # Returns the average value of an amoutn of the same die
    return number * ((1 + die) / 2)


def mult_avg(instructions):  # Returns the average of an arbitrary roll
    total = 0
    for instruction in instructions:
        if instruction.find("+") >= 0:
            numbers = re.sub("\D", "", instruction)
            total += int(numbers)
        elif instruction.find("-") >= 0:
            numbers = re.sub("\D", "", instruction)
            total -= int(numbers)
        elif instruction.find("d") > 0:
            args = instruction.split("d")
            result = s_avg(int(args[0]), int(args[1]))
            total += result
        else:
            pass
            # print("invalid")
    return total


def avg_from_list(name, dict, var):
    return mult_avg(replace_variables(dict.get(name), var))


def avg_from_string(input, var):
    inputs = input.split(" ")
    return mult_avg(replace_variables(inputs, var))


def random_from_file(filepaths):  # Picks entry in rolling table
    filepaths = filepaths.split(" ")
    choices = []
    for file in filepaths:
        picked = random.choice(open(file).readlines())
        picked = re.sub("(\n|\W)", "", picked)
        choices.append(picked)
    return " ".join(choices)


def deathsave():
    failures = 0
    successes = 0
    adv = input("Do you have advantage on death saves? (yes/no)")
    while failures < 3 and successes < 3:
        input("Press Enter for your next death save")
        result = s_roll(1, 20)
        if adv == "yes":
            advroll = s_roll(1, 20)
            if advroll > result:
                result = advroll
        print("You rolled " + str(result))
        if result < 10:
            failures += 1
        else:
            successes += 1
        print(f"Failures: {failures} | Successes: {successes}")
    if successes == 3:
        print("You are stable")
    if failures == 3:
        print("You are dead")
