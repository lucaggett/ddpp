import random
import re
import timeit
from statistics import median
from typing import Dict, Any
import pprint


class ddpp():  # Saves Required Data (config dicts)
    def __init__(self):
        self.config = {}
        self.i = 0
        self.variables = {}

    def importddpp(self):
        '''
        imports the config.ddpp file as a the config dictionary,
        as well as the character.var and custom.var as a dictionary of variables.
        '''
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
    """
    returns an int
    generates a random number based on amount of sides of the die and the number of dice
    """
    total = 0
    for i in range(0, number):
        roll = random.randrange(1, die, 1)
        total += roll
    return total


def mult_roll(instructions):  # Rolls arbitrary Combinations of dice
    """
    returns 2 variables: total (an integer) and rolls (a string)

    returns a number and a string, based on rolls and modifiers parsed from instructions
    """
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
    """
    returns sanitized input, an instruction set which mult_roll can accept

    replaces variables with numbers parsed from a .var file and recreates the output
    """
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


def roll_from_string(inputt, var):  # Rolls Roll defined in String
    inputs = inputt.split(" ")
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


def initiative_tracker():
    initiative_temp = {}
    active = True
    initiative = {}
    number = input("enter the number of entities in the initiative: ")
    for i in range(0, int(number)):
        name = input("enter your entities name")
        speed = input("enter the initiative of your character")
        if speed == "roll":
            modifier = input("Enter your creature's initiative modifier")
            roll_from_string()
        initiative.update({name: speed})
    print("beginning initiative")
    i = 0
    # noinspection PyTypeChecker
    initiative = dict(sorted(initiative.items(), key=lambda item: item[1], reverse=True))
    initiative_temp.update(initiative)
    while active:
        initiative.update(initiative_temp)
        initiative = dict(sorted(initiative.items(), key=lambda item: item[1], reverse=True))
        for entity in initiative:
            print("Entity:", entity, "| Initiative:", initiative.get(entity))
            x = input()
            if x == "help":
                print("possible commands: add, remove, print, exit (press enter for next creature)")
            if x == "add":
                name = input("enter the name of your creature: ")
                speed = input("enter the initiative of your creature: ")
                initiative_temp.update({name: speed})
                # noinspection PyTypeChecker
                initiative_temp = dict(sorted(initiative_temp.items(), key=lambda item: item[1], reverse=True))
            if x == "remove":
                toRemove = input("enter the name of the creature you want to remove: ")
                print(toRemove)
                pprint.pprint(initiative_temp, width=1)
                if initiative_temp.pop(toRemove, -100) == -100:
                    print("entity not found")
                else:
                    print(f"{toRemove} will be removed at the start of the initiative")
            if x == "print":
                pprint.pprint(initiative, width=1)
            if x == "exit":
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
        if adv == "yes" or adv == "yup":
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

def tester():
    x = ()
    list = []
    for i in range(1,100):
        x = mult_roll("1d100")
        list.append(int(x[0]))
    print(median(list))



