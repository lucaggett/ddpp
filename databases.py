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


class Database(ABC):
    """
    this class handles the loading of databases
    """

    available_sources_creatures = os.listdir(f"{JSONPATH}/bestiary")
    available_sources_spells = os.listdir(f"{JSONPATH}/spells")
    database_type = None

    def __init__(self, database_name: str, filepath: str = JSONPATH, sources=None):
        """
        initializes the database
        """
        self.database_name = database_name
        self.filepath = filepath
        self.sources = sources if sources else self.get_available_sources()
        self.database = {}

    @abstractmethod
    def get_available_sources(self) -> list:
        """
        returns a list of available sources for the database
        """
        pass

    def get_random_entity(self) -> dict:
        """
        returns a random entity from the database
        """
        return choice(list(self.database.values()))

    def import_source_data(self) -> dict:
        """
        returns a dictionary of the source data for the database
        """
        source_data = {}
        for source in self.sources:
            if "bestiary" not in source.split("-")[0]:
                # if the source file name does not contain bestiary, we skip it
                continue
            data = []
            with open(os.path.join(JSONPATH, self.database_type, source)) as f:
                print(os.path.join(JSONPATH, self.database_type, source))
                data += json.load(f).get("monster")
        print(random.choice(data))
        for entry in source_data.items():
            print(entry)
            if entry[0] not in self.database:
                self.database[source_data["name"]] = source_data[entry]
        return self.database


        def create_creature_object(self, creature: dict):
            pass

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

    def get_available_sources(self) -> list:
        """
        returns a list of available sources for the database
        """
        return self.available_sources_creatures




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