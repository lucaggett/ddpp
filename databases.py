"""
this module contains the class that handles databases of monsters and items
"""

import json
import os

# path from project root to database files
import random
from abc import ABC, abstractmethod
import os
from random import choice

projectroot = os.path.abspath(os.path.join(os.path.dirname(__file__)))
JSONPATH = str(projectroot) + r"/JSON"


def normalize_cr(cr):
    if cr == "Unknown":
        return 0
    if type(cr) is dict:
        cr = normalize_cr(cr['cr'])
    elif not '/' in cr:
        cr = float(cr)
    else:
        cr_list = cr.split('/')
        cr = float(int(cr_list[0]) / int(cr_list[1]))
    return cr


def normalize_visual_cr(cr):
    if type(cr) is dict:
        cr = normalize_visual_cr(cr['cr'])

    return cr


def get_type(typus):
    if type(typus) is dict:
        return get_type(typus['type'])
    else:
        return typus


def get_ac(ac):
    if type(ac) is dict:
        return get_ac(ac['ac'])
    else:
        return ac


class Database(ABC):
    """
    this class handles the loading of databases
    """
    available_sources_creatures = os.listdir(rf"{JSONPATH}\bestiary")
    available_sources_spells = os.listdir(rf"{JSONPATH}\spells")

    def __init__(self, database_name: str, filepath: str = JSONPATH, sources=None):
        """
        initializes the database
        """
        self.database_name = database_name
        self.filepath = filepath
        if not sources:
            self.get_available_sources()
        else:
            self.sources = sources
        self.db = {}

    def get_available_sources(self):
        """
        returns a list of available sources for the database
        """
        self.sources = [file for file in os.listdir(rf"{self.filepath}\{self.database_type}") if file.startswith("bestiary")]
        print(self.sources)
        return self


    def get_random_entity(self) -> dict:
        """
        returns a random entity from the database
        """
        return choice(list(self.database.values()))

    def import_source_data(self):
        """
        returns a dictionary of the source data for the database
        """
        if not self.database_type:
            raise NotImplementedError("database_type not set, all subclasses of database must set this")
        source_data = []
        monsters = {}
        for source in self.sources:
            with open(fr"{self.filepath}\{self.database_type}\{source}", "r", encoding="utf-8") as file:
                source_data.append(json.load(file)["monster"])
        for part in source_data:
            for monster in part:
                monsters.update({monster["name"]: monster})
        self.db = monsters
        return self

class Bestiary(Database):
    """
    this class handles the loading of the bestiary database
    """

    def __init__(self, database_name: str, filepath: str = JSONPATH, sources=None):
        """
        initializes the bestiary database
        """
        self.database_type = "bestiary"
        super().__init__(database_name, filepath, sources)


    def search_by_name(self, name: str) -> dict:
        """
        returns a dictionary of the monster with the given name
        """
        return self.db[name]

    def search_by_cr(self, cr: int) -> dict or list[dict]:
        """
        returns a dictionary of the monster with the given challenge rating
        """
        output = []
        for monster in self.db.values():
            if normalize_cr(monster.get('cr', '1000')) == cr:
                output.append(monster)
        return output




class Spells(Database):
    """
    spell loading handler
    """

    def __init__(self, database_name, filepath=JSONPATH, sources=None):
        """
        initializes the spell database
        """
        super().__init__(database_name, filepath, sources)
        self.database_type = "spells"


    def get_available_sources(self) -> list:
        """
        returns a list of available sources for the database
        """
        return self.available_sources_spells


if __name__ == "__main__":
    bestiary = Bestiary("bestiary")
    bestiary.import_source_data()


if __name__ == "__main__":
    bestiary = Bestiary("bestiary")
    print(bestiary.get_available_sources())
    bestiary.import_source_data()
    print(bestiary.search_by_name("Bearded Devil"))
    print(random.choice(bestiary.search_by_cr(2)))
