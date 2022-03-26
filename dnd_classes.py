"""
Object-Oriented implementation of DnD classes.
"""

from abc import ABC, abstractmethod
from ddpp_classes import Weapon


# pylint: disable=invalid-name
class dnd_Character(ABC):  # a 5e Character, can be imported from file
    """
    returns a Character object, with most of the stats from a 5e Character sheet.
    Weopons are created using the Weapon class.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name="",
        level=1,
        stats=None,
        armor_class=0,
        health=0,
        proficiency_bonus=0,
        proficiencies=None,
        weapon=None,
    ) -> None:
        if stats is None:
            stats = {
                "strength": 0,
                "dexterity": 0,
                "constitution": 0,
                "intelligence": 0,
                "wisdom": 0,
                "charisma": 0,
            }
        self.name = name
        self.level = level
        self.armor_class = armor_class
        self.health = health
        self.stats = stats
        self.proficiency_bonus = proficiency_bonus
        self.proficiencies = [] if not proficiencies else proficiencies
        self.weapon = weapon if weapon else None

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
            for stat, value in stats.items():
                if stat == "weapon":
                    file.write(f"Weapon {self.weapon.export()}")
                else:
                    file.write(f"{stat} {value}\n")

    def create_character(self) -> None:
        """
        creates a Character object.
        """

        self.name = input("Enter Character Name: ")
        for stat in self.stats:
            self.stats[stat] = int(input(f"Enter {stat}: "))
        self.proficiency_bonus = int(input("Enter Proficiency_bonus Bonus: "))
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
        if isinstance(self.weapon, Weapon):
            return self.weapon.attack()
        return self.stats["strength"]
