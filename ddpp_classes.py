import ddpp

class config():  # Saves Required Data (config dicts)
    def __init__(self):
        self.config = {}
        self.variables = {}
        with open("config.ddpp") as config:
            for line in config:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1:len(line_tok)]}
                self.config.update(localdict)
        with open("custom.var") as custom:
            for variable in custom:
                var = var.replace("\n", "")
                var = var.split(" ")
                localvar = {var[0]: var[1]}
                self.variables.update(localvar)

class weapon():
    def __init__(self, name, attack, damage, crit_range):
        self.name = name
        self.attack = attack
        self.damage = damage
        self.crit_range = crit_range

    def attack(self):
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

class character():  # a 5e character, can be imported from file
    """
    returns a character object, with most of the stats from a 5e character sheet. Weopons are created using the weapon
    class.
    """

    def __init__(self):
        self.Strength = 0
        self.Dexterity = 0
        self.Constitution = 0
        self.Intelligence = 0
        self.Wisdom = 0
        self.Charisma = 0
        self.Hitpoints = 0
        self.Proficiency = 0
        self.Initiative = 0
        self.Speed = 0
        self.Armor = 0
        self.Shield = 0
        self.Weapon = weapon("Null", 0, 0, 0)

    def import_stats(self, character_name):
        """
        imports character stats from a file.
        """
        with open(character_name) as character:
            for line in character:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                if line_tok[0] == "Strength":
                    self.Strength = int(line_tok[1])
                elif line_tok[0] == "Dexterity":
                    self.Dexterity = int(line_tok[1])
                elif line_tok[0] == "Constitution":
                    self.Constitution = int(line_tok[1])
                elif line_tok[0] == "Intelligence":
                    self.Intelligence = int(line_tok[1])
                elif line_tok[0] == "Wisdom":
                    self.Wisdom = int(line_tok[1])
                elif line_tok[0] == "Charisma":
                    self.Charisma = int(line_tok[1])
                elif line_tok[0] == "Hitpoints":
                    self.Hitpoints = int(line_tok[1])
                elif line_tok[0] == "Proficiency":
                    self.Proficiency = int(line_tok[1])
                elif line_tok[0] == "Initiative":
                    self.Initiative = int(line_tok[1])
                elif line_tok[0] == "Speed":
                    self.Speed = int(line_tok[1])
                elif line_tok[0] == "Armor":
                    self.Armor = int(line_tok[1])
                elif line_tok[0] == "Shield":
                    self.Shield = int(line_tok[1])
                elif line_tok[0] == "Weapon":
                    self.Weapon = weapon(line_tok[1], int(line_tok[2]), int(line_tok[3]), line_tok[4])
                else:
                    print("Error: Invalid Stat")

    def attack(self):
        """
        makes an attack!
        """
        return self.Weapon.attack()

