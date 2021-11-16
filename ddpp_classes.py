# *-* coding: utf-8 *-*
# pylint: disable=line-too-long
# pylint: disable=R0902
# pylint: disable=R0912
"""
The Module containing the classes for ddpp.py,
creating objects for characters and objects
"""
import os.path
from os.path import exists
import sys
import ddpp


class Config:
    """
    the config function, for creating a config object which holds the configuration data
    for ddpp.py, as well as the variables defined in custom.var in useable objects.
    """

    def __init__(self):
        self.config_file = {}
        self.variables = {}

    def create_config(self):
        """
        creates a new shortcut in the config file
        """
        alias = input("What is the name of the shortcut? ")
        command = input(
            "Please enter your shortcut\nExamples:\n1.) 1d8 +2\n2.) 1d10 +[strength]\n3.) 1d20 +[dexterity] +[proficiency]\n>> "
        )
        self.config_file[alias] = command
        self.export_config()

    def import_config(self):
        """
        Imports the config file and returns the imported data.
        """
        if not exists("config/config.ddpp"):
            sys.exit("config.ddpp does not exist, exiting")
        with open("config/config.ddpp", encoding="utf-8") as config_data:
            for line in config_data:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1 : len(line_tok)]}
                self.config_file.update(localdict)
        return self.config_file

    def create_variable(self):
        """
        creates a new variable in thse variable and saves it to the variables file
        """
        name = input("What is the name of the variable? ")
        value = input("What is the value of the variable? ")
        self.variables[name] = value
        self.export_variables()

    def import_variables(self):
        """
        Imports the variables file, and then returns the imported data
        """
        if not exists("config/variables.ddpp"):
            sys.exit("variables.ddpp does not exist, exiting")
        with open("config/variables.ddpp", encoding="utf-8") as custom:
            for var in custom:
                var = var.replace("\n", "")
                var = var.split(" ")
                localvar = {var[0]: var[1]}
                self.variables.update(localvar)
        return self.variables

    def delete_variable(self):
        """
        deletes a variable from the variables file
        """
        name = input("What is the name of the variable? ")
        del self.variables[name]
        self.export_variables()

    def delete_config(self):
        """
        deletes a config from the config file
        """
        alias = input("What is the name of the shortcut? ")
        del self.config_file[alias]
        self.export_config()

    def export_variables(self):
        """
        exports the currently stored variables to a text file
        """
        if not exists("config/variables.ddpp"):
            print(
                "variables.ddpp does not exist, creating new file at "
                + os.path.abspath("config/variables.ddpp")
            )
        with open("config/variables.ddpp", "w", encoding="utf-8") as file:
            for item in self.variables:
                file.write(f"{item} {self.variables[item]}")

    def print_config(self):
        """
        prints the currently imported configuration data
        """
        print(self.config_file)
        print(self.variables)

    def export_config(self):
        """
        exports the currently imported configuration data to a file
        """
        if not exists("config/config.ddpp"):
            print(
                "config.ddpp does not exist, creating new file at "
                + os.path.abspath("config/config.ddpp")
            )
        with open("config/config.ddpp", "w", encoding="utf-8") as file:
            for item in self.config_file:
                file.write(f"{item} {self.config_file[item]}\n")
        print("exported config to config.ddpp")


class Weapon:
    """
    A class representing a Weapon in 5e, contains fields
    name: str
    attack: string (format: XdY)
    damage: string (format: XdY)
    crit_range: list[int]
    """

    def __init__(self, name, attack, damage, crit_range):
        self.name = name
        self.attack = attack
        self.damage = damage
        fixed_crit_range = crit_range
        for item in fixed_crit_range:  # kind of a shitty way to do this, but whatever
            fixed_crit_range[fixed_crit_range.index(item)] = int(item)
        self.crit_range = fixed_crit_range

    def attack_roll(self):
        """
        rolls an attack using the Weapon, returns all results and rolls
        :return:
        """
        attack_roll, attack_dice = ddpp.mult_roll(self.attack)
        damage_roll, damage_dice = ddpp.mult_roll(self.damage)
        for number in self.crit_range:
            if int(number) == attack_roll:
                damage_roll = damage_roll * 2
        return attack_roll, attack_dice, damage_roll, damage_dice

    def export(self):
        """
        helps export the Weapon to a Character.config file. Returns a string
        containing the weapons Name, attack , damage, and crit range
        :return:
        """
        crit_range = ""
        for item in self.crit_range:
            crit_range += str(item) + " "
        crit_range = crit_range[:-1]
        return f"{self.name} {self.attack} {self.damage} {crit_range}"


class Character:  # a 5e Character, can be imported from file
    """
    returns a Character object, with most of the stats from a 5e Character sheet.
    Weopons are created using the Weapon class.
    """

    def __init__(self):
        self.name = ""
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.health_points = 0
        self.proficiency = 0
        self.initiative = 0
        self.speed = 0
        self.armor_class = 0
        self.weapon = Weapon(
            "If you see this something went wrong",
            "1d100",
            "1d100",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )

    def import_char(self, filepath):
        """
        imports Character stats from a file.
        """
        with open(filepath, encoding="utf-8") as character:
            for line in character:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                if line_tok[0] == "strength":
                    self.strength = int(line_tok[1])
                elif line_tok[0] == "name":
                    self.name = line_tok[1]
                elif line_tok[0] == "dexterity":
                    self.dexterity = int(line_tok[1])
                elif line_tok[0] == "constitution":
                    self.constitution = int(line_tok[1])
                elif line_tok[0] == "intelligence":
                    self.intelligence = int(line_tok[1])
                elif line_tok[0] == "wisdom":
                    self.wisdom = int(line_tok[1])
                elif line_tok[0] == "charisma":
                    self.charisma = int(line_tok[1])
                elif line_tok[0] == "health_points":
                    self.health_points = int(line_tok[1])
                elif line_tok[0] == "proficiency":
                    self.proficiency = int(line_tok[1])
                elif line_tok[0] == "initiative":
                    self.initiative = int(line_tok[1])
                elif line_tok[0] == "speed":
                    self.speed = int(line_tok[1])
                elif line_tok[0] == "armor_class":
                    self.armor_class = int(line_tok[1])
                elif line_tok[0] == "Weapon":
                    self.weapon = Weapon(
                        line_tok[1], line_tok[2], line_tok[3], line_tok[4:]
                    )
                else:
                    print("Error: Invalid Stat " + line_tok[0])

    def export_character(self):
        """
        writes the Character file from the object to the file system.
        """
        stats = vars(self)
        with open(f"text/{self.name}.txt", "w", encoding="utf-8") as file:
            for stat in stats:
                if stat == "weapon":
                    file.write(f"Weapon {self.weapon.export()}")
                else:
                    file.write(f"{stat} {stats[stat]}\n")

    def create_character(self):
        """
        creates a Character object.
        """
        self.name = input("Enter Character Name: ")
        self.strength = int(input("Enter Strength: "))
        self.dexterity = int(input("Enter Dexterity: "))
        self.constitution = int(input("Enter Constitution: "))
        self.intelligence = int(input("Enter Intelligence: "))
        self.wisdom = int(input("Enter Wisdom: "))
        self.charisma = int(input("Enter Charisma: "))
        self.health_points = int(input("Enter Hitpoints: "))
        self.proficiency = int(input("Enter Proficiency_bonus Bonus: "))
        self.initiative = int(input("Enter Initiative: "))
        self.speed = int(input("Enter Speed: "))
        self.armor_class = int(input("Enter armor_class: "))
        self.weapon = Weapon(
            input("Enter Weapon Name: "),
            input("Enter Weapon Attack: "),
            input("Enter Weapon Damage: "),
            input("Enter Weapon Crit Range: ").split(","),
        )

    def attack(self):
        """
        makes an attack!
        """
        return self.weapon.attack_roll()
