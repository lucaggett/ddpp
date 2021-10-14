import random
import re
from typing import Dict, Any


class ddpp():
    def __init__(self):
        self.dict = {}
        self.i = 0
        self.variables = {}

    def importddpp(self):
        with open("config.ddpp") as config:
            for line in config:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1:len(line_tok)]}
                self.dict.update(localdict)
                self.i += 1

        with open("character.var") as character:
            for stat in character:
                stat = stat.replace("\n", "")
                stat = stat.split(" ")
                localstat = {stat[0]: stat[1]}
                self.variables.update(localstat)


def s_roll(number, die):
    total = 0
    for i in range(0, number):
        roll = random.randrange(1, die, 1)
        total += roll
    return total


def mult_roll(instructions):
    total = 0
    rolls = ""
    for instruction in instructions:
        if instruction.find("+") >= 0:
            # print("addition")
            numbers = re.sub("\D", "", instruction)
            total += int(numbers)
            rolls += str(numbers) + " + "
            # print(total)
        elif instruction.find("-") >= 0:
            # print("subtraction")
            numbers = re.sub("\D", "", instruction)
            total -= int(numbers)
            rolls += str(numbers) + " + "
            # print(total)
        elif instruction.find("d") > 0:
            # print("dice")
            args = instruction.split("d")
            # print(args)
            # print(s_roll(int(args[0]), int(args[1])))
            result = s_roll(int(args[0]), int(args[1]))
            total += result
            rolls += str(result) + " + "
        else:
            pass
            # print("invalid")
    return total, rolls[:-3]


def replace_variables(instructions, variables):
    sanitized = []
    for instruction in instructions:
        instruction_positive = True
        variable_positive = True
        if instruction.find("[") >= 0:
            if instruction.find("-") >= 0:
                instruction_positive = False
            variable_name = re.sub("[^A-Za-z]", "", instruction)
            variable = str(variables.get(variable_name))
            if variable.find("-"):
                variable_positive = False
            variable = re.sub("\D", "", variable)
            if variable_positive == instruction_positive:
                sanitized.append("+" + str(variable))
            else:
                sanitized.append("+" + str(variable))
        else:
            sanitized.append(instruction)
    return sanitized


def roll_from_dict(name, dict, var):
    # print(dict.get(name))
    return mult_roll(replace_variables(dict.get(name), var))


def roll_from_string(input, var):
    inputs = input.split(" ")
    return mult_roll(replace_variables(inputs, var))


def s_avg(number, die):
    # returns the average value of an amoutn of the same die
    return number * ((1 + die) / 2);


def mult_avg(instructions):
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


def avg_from_dict(name, dict, var):
    return mult_avg(replace_variables(dict.get(name), var))


def avg_from_string(input, var):
    inputs = input.split(" ")
    return mult_avg(replace_variables(inputs,var))


def random_from_file(filepaths):
    filepaths = filepaths.split(" ")
    choices = []
    for file in filepaths:
        picked = random.choice(open(file).readlines())
        picked = re.sub("(\n|\W)", "", picked)
        choices.append(picked)
    return " ".join(choices)




instance = ddpp()
ddpp.importddpp(instance)
# print(instance.dict)
# rint(type(instance.dict))
print("Roll from dict: " + str(roll_from_dict("test", instance.dict, instance.variables)[0]))
print("Roll fromString: " + str(roll_from_string("1d12 +2", instance.variables)) + "       '1d12 +2'")
print("Average from dict: " + str(avg_from_dict("big", instance.dict, instance.variables)))
print("Average fom string w/ replace var: " + str(avg_from_string("1d1 +[DEX]", instance.variables)) + "    '1d1 +[DEX]'")
print("Replace Var: " + str(roll_from_dict("strength_check", instance.dict, instance.variables)))