# *-* coding: utf-8 *-*
# pylint: disable=line-too-long
# pylint: disable=R0902
# pylint: disable=R0912
"""
The Module containing the classes for ddpp.py,
creating objects for characters and objects
"""
import os.path
import platform
from abc import ABC, abstractmethod
from os.path import exists
import sys
from ddpp import *


class Config:
    """
    the config function, for creating a config object which holds the configuration data
    for ddpp.py, as well as the variables defined in custom.var in useable objects.
    """

    def __init__(self):
        self.config_file = {}
        self.variables = {}
        self.filepath = ""

        if platform.system() == "windows":
            if not os.path.exists(r"C:\Program Files\ddpp"):
                os.makedirs(r"C:\Program Files\ddpp")
            self.filepath = r"C:\Program Files\ddpp\config.ddpp"
        if platform.system() == "Linux" or platform.system() == "linux":
            if not os.path.exists(r"/usr/local/bin/ddpp"):
                os.makedirs(r"/usr/local/bin/ddpp")
            self.filepath = r"/usr/local/bin/ddpp/"

    def create_config(self) -> None:
        """
        creates a new shortcut in the config file
        """
        alias = input("What is the name of the shortcut? ")
        command = input(
            "Please enter your shortcut\nExamples:\n1.) 1d8 +2\n2.) 1d10 +[strength]\n3.) 1d20 +[dexterity] +[proficiency]\n>> "
        )
        self.config_file[alias] = command
        self.export_config()

    def import_config(self) -> dict:
        """
        Imports the config file and returns the imported data.
        """
        if not exists(f"{self.filepath}config.ddpp"):
            b = open(f"{self.filepath}config.ddpp", "x", encoding="utf-8")
            b.close()
        with open(f"{self.filepath}config.ddpp", encoding="utf-8") as config_data:
            for line in config_data:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1 : len(line_tok)]}
                self.config_file.update(localdict)
        return self.config_file

    def create_variable(self) -> None:
        """
        creates a new variable in thse variable and saves it to the variables file
        """
        name = input("What is the name of the variable? ")
        value = input("What is the value of the variable? ")
        self.variables[name] = value
        self.export_variables()

    def import_variables(self) -> dict:
        """
        Imports the variables file, and then returns the imported data
        """
        if not exists(f"{self.filepath}variables.ddpp"):
            b = open(f"{self.filepath}variables.ddpp", "x", encoding="utf-8")
            b.close()
        with open("config/variables.ddpp", encoding="utf-8") as custom:
            for var in custom:
                var = var.replace("\n", "")
                var = var.split(" ")
                localvar = {var[0]: var[1]}
                self.variables.update(localvar)
        return self.variables

    def delete_variable(self) -> None:
        """
        deletes a variable from the variables file
        """
        name = input("What is the name of the variable? ")
        del self.variables[name]
        self.export_variables()

    def delete_config(self) -> None:
        """
        deletes a config from the config file
        """
        alias = input("What is the name of the shortcut? ")
        del self.config_file[alias]
        self.export_config()

    def export_variables(self) -> None:
        """
        exports the currently stored variables to a text file
        """
        if not exists(f"{self.filepath}/variables.ddpp"):
            print(
                "variables.ddpp does not exist, creating new file at "
                + os.path.abspath("config/variables.ddpp")
            )
        with open(f"{self.filepath}/variables.ddpp", "w", encoding="utf-8") as file:
            for item in self.variables:
                file.write(f"{item} {self.variables[item]}\n")

    def print_config(self) -> None:
        """
        prints the currently imported configuration data
        """
        print(self.config_file)
        print(self.variables)

    def export_config(self) -> None:
        """
        exports the currently imported configuration data to a file
        """
        if not exists(f"{self.filepath}/config.ddpp"):
            print("config.ddpp does not exist, creating new file at " + self.filepath)
        with open(f"{self.filepath}/config.ddpp", "w", encoding="utf-8") as file:
            for item in self.config_file:
                file.write(f"{item} {self.config_file[item]}\n")
        print(f"exported config to {self.filepath}config.ddpp")


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
            if not isinstance(item, int):
                fixed_crit_range[fixed_crit_range.index(item)] = int(item)
        self.crit_range = fixed_crit_range

    def attack_roll(self) -> tuple[int, str, int, str]:
        """
        rolls an attack using the Weapon, returns all results and rolls
        :return:
        """
        attack_roll, attack_dice = mult_roll(self.attack)
        damage_roll, damage_dice = mult_roll(self.damage)
        for number in self.crit_range:
            if int(number) == attack_roll:
                damage_roll = damage_roll * 2
        return attack_roll, attack_dice, damage_roll, damage_dice

    def export(self) -> str:
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


class Character(ABC):  # a 5e Character, can be imported from file
    """
    returns a Character object, with most of the stats from a 5e Character sheet.
    Weopons are created using the Weapon class.
    """

    def __init__(self):
        self.name = ""
        self.stats = {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
        }
        self.speed = 0
        self.armor_class = 0
        self.hp = 0
        self.proficiency = 0
        self.speed = 0
        self.armor_class = 0
        self.weapon = Weapon(
            "If you see this something went wrong",
            "1d100",
            "1d100",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )

    def import_char(self, filepath) -> None:
        """
        imports Character stats from a file.
        """
        with open(filepath, encoding="utf-8") as character:
            attrs = vars(self)
            for line in character:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                if line_tok[0] in self.stats:
                    self.stats[line_tok[0]] = line_tok[1]
                elif line_tok[0] in attrs:
                    self.__setattr__(line_tok[0], line_tok[1])

    def export_character(self) -> None:
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

    def create_character(self) -> None:
        """
        creates a Character object.
        """

        self.name = input("Enter Character Name: ")
        for stat in self.stats:
            self.stats[stat] = input(f"Enter {stat}: ")
        self.proficiency = int(input("Enter Proficiency_bonus Bonus: "))
        self.speed = int(input("Enter Speed: "))
        self.armor_class = int(input("Enter armor_class: "))
        self.weapon = Weapon(
            input("Enter Weapon Name: "),
            input("Enter Weapon Attack: "),
            input("Enter Weapon Damage: "),
            input("Enter Weapon Crit Range: ").split(","),
        )

    @abstractmethod
    def attack(self) -> int:
        """
        makes an attack!
        """
        pass
