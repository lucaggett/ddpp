"""
this module contains the class that handles databases of monsters and items
"""

import json
import os

# path from project root to database files
from abc import ABC, abstractmethod
import os
from random import choice

projectroot = os.path.abspath(os.path.join(os.path.dirname(__file__)))
JSONPATH = str(projectroot) + "\\JSON"


class Database(ABC):
    """
    this class handles the loading of databases
    """
    available_sources_creatures = os.listdir(f"{JSONPATH}\bestiary")
    available_sources_spells = os.listdir(f"{JSONPATH}\spells")


    def __init__(self, database_name: str, filepath: str = JSONPATH, sources=None):
        """
        initializes the database
        """
        self.database_name = database_name
        self.filepath = filepath
        self.sources = sources
        self.db = {}


    def get_available_sources(self) -> list:
        """
        returns a list of available sources for the database
        """
        return os.listdir(f"{self.filepath}\{self.database_type}")

    def get_random_entity(self) -> dict:
        """
        returns a random entity from the database
        """
        return choice(list(self.db.values()))

    def import_source_data(self) -> dict:
        """
        returns a dictionary of the source data for the database
        """
        if not self.database_type:
            raise NotImplementedError("database_type not set, all subclasses of database must set this")
        source_data = {}
        for source in self.sources:
            source_data = json.loads(rf"{self.filepath}\{self.database_type}\{source}")
            for creature in source_data:
                if creature not in self.db:
                    self.db[creature] = source_data[creature]
        return self.db


class Bestiary(Database):
    """
    this class handles the loading of the bestiary database
    """

    def __init__(self, database_name: str, filepath: str = JSONPATH, sources=None):
        """
        initializes the bestiary database
        """
        super().__init__(database_name, filepath, sources)
        self.database_type = "bestiary"

    def get_available_sources(self) -> list:
        """
        returns a list of available sources for the database
        """
        return self.available_sources_creatures


class Spells(Database):
    """
    this class handles the loading of the spells database
    """

    def __init__(self, database_name: str, filepath: str = JSONPATH, sources=None):
        """
        initializes the spells database
        """
        super().__init__(database_name, filepath, sources)
        self.database_type = "spells"