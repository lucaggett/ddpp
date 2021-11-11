import ddpp
"""
The Module containing the classes for ddpp.py, 
creating objects for characters and objects
"""

class config():
    """
    the config function, for creating a config object which holds the configuration data
    for ddpp.py, as well as the variables defined in custom.var in useable objects.
    """
    def __init__(self):
        self.configFile = {}
        self.variables = {}

    def import_config(self):
        """
        Imports the config file and returns the imported data.
        """
        with open("config/config.ddpp") as config:
            for line in config:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1:len(line_tok)]}
                self.configFile.update(localdict)
        return self.configFile


    def import_variables(self):
        """
        Imports the variables file, and then returns the imported data
        """
        with open("config/variables.ddpp") as custom:
            for variable in custom:
                var = var.replace("\n", "")
                var = var.split(" ")
                localvar = {var[0]: var[1]}
                self.variables.update(localvar)
        return self.variables


    def print_config(self):
        """
        prints the currently imported configuration data
        """
        print(self.configFile)
        print(self.variables)

    def export_config(self):
        with open("config.ddpp", "w") as file:
            for item in self.configFile.items():
                file.write(f'{item} {self.configFile[item]}')


class weapon():
    """
    A class representing a weapon 5e, contains fields
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
        rolls an attack using the weapon, returns all results and rolls
        :return:
        """
        attack_roll, attack_dice = ddpp.mult_roll(self.attack)
        damage_roll, damage_dice = ddpp.mult_roll(self.damage)
        for number in self.crit_range:
            if str(number) in attack_roll:
                damage_roll = damage_roll * 2
        return attack_roll, attack_dice, damage_roll, damage_dice

    def export(self):
        """
        helps export the weapon to a character.config file. Returns a string
        containing the weapons Name, attack , damage, and crit range
        :return:
        """
        crit_range = ""
        for item in self.crit_range:
            crit_range += str(item) + " "
        crit_range = crit_range[:-1]
        return f"{self.name} {self.attack} {self.damage} {crit_range}"


class character():  # a 5e character, can be imported from file
    """
    returns a character object, with most of the stats from a 5e character sheet.
    Weopons are created using the weapon class.
    """

    def __init__(self):
        self.name = ""
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.HP = 0
        self.proficiency = 0
        self.initiative = 0
        self.speed = 0
        self.AC = 0
        self.weapon = weapon("If you see this something went wrong", "1d100", "1d100", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def import_char(self, filepath):
        """
        imports character stats from a file.
        """
        with open(filepath) as character:
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
                elif line_tok[0] == "HP":
                    self.HP = int(line_tok[1])
                elif line_tok[0] == "proficiency":
                    self.proficiency = int(line_tok[1])
                elif line_tok[0] == "initiative":
                    self.initiative = int(line_tok[1])
                elif line_tok[0] == "speed":
                    self.speed = int(line_tok[1])
                elif line_tok[0] == "AC":
                    self.AC = int(line_tok[1])
                elif line_tok[0] == "weapon":
                    self.weapon = weapon(line_tok[1], line_tok[2], line_tok[3], line_tok[4:])
                else:
                    print("Error: Invalid Stat " + line_tok[0])

    def export_character(self):
        """
        writes the character file from the object to the file system.
        """
        stats = vars(self)
        with open(f"text/{self.name}.txt", "w") as file:
            for stat in stats:
                if stat == "weapon":
                    file.write(f"weapon {self.weapon.export()}")
                else:
                    file.write(f"{stat} {stats[stat]}\n")

    def create_character(self):
        """
        creates a character object.
        """
        self.name = input("Enter Character Name: ")
        self.strength = int(input("Enter Strength: "))
        self.dexterity = int(input("Enter Dexterity: "))
        self.constitution = int(input("Enter Constitution: "))
        self.intelligence = int(input("Enter Intelligence: "))
        self.wisdom = int(input("Enter Wisdom: "))
        self.charisma = int(input("Enter Charisma: "))
        self.HP = int(input("Enter Hitpoints: "))
        self.proficiency = int(input("Enter Proficiency_bonus Bonus: "))
        self.initiative = int(input("Enter Initiative: "))
        self.speed = int(input("Enter Speed: "))
        self.AC = int(input("Enter AC: "))
        self.weapon = weapon(input("Enter Weapon Name: "),
                             input("Enter Weapon Attack: "),
                             input("Enter Weapon Damage: "),
                             input("Enter Weapon Crit Range: ").split(","))

    def attack(self):
        """
        makes an attack!
        """
        return self.weapon.attack()
