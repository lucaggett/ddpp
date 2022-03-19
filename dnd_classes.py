from abc import ABC, abstractmethod
from ddpp_classes import Weapon
from ddpp import Instructions


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
        self.proficiencies = []
        self.saving_throws = []
        self.weapon = Weapon(
            "Invalid",
            "Invalid",
            "Invalid",
            "Invalid",
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
