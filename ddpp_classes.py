import ddpp


class config():  # Saves Required Data (config dicts)
    def __init__(self):
        self.configFile = {}
        self.variables = {}

    def import_config(self):

        with open("config/config.ddpp") as config:
            for line in config:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                localdict = {line_tok[0]: line_tok[1:len(line_tok)]}
                self.configFile.update(localdict)
        with open("config/custom.var") as custom:
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
        fixed_crit_range = crit_range
        for item in fixed_crit_range:  # kind of a shitty way to do this, but whatever
            fixed_crit_range[fixed_crit_range.index(item)] = int(item)
        self.crit_range = fixed_crit_range

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
    returns a character object, with most of the stats from a 5e character sheet. Weopons are created using the weapon
    class.
    """

    def __init__(self):
        self.Name = ""
        self.Strength = 0
        self.Dexterity = 0
        self.Constitution = 0
        self.Intelligence = 0
        self.Wisdom = 0
        self.Charisma = 0
        self.Hitpoints = 0
        self.Proficiency_bonus = 0
        self.Initiative = 0
        self.Speed = 0
        self.AC = 0
        self.Weapon = weapon("If you see this something went wrong", "1d100", "1d100", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def import_char(self, filepath):
        """
        imports character stats from a file.
        """
        with open(filepath) as character:
            for line in character:
                line = line.replace("\n", "")
                line_tok = line.split(" ")
                if line_tok[0] == "Strength":
                    self.Strength = int(line_tok[1])
                elif line_tok[0] == "Name":
                    self.Name = line_tok[1]
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
                elif line_tok[0] == "Proficiency_bonus":
                    self.Proficiency_bonus = int(line_tok[1])
                elif line_tok[0] == "Initiative":
                    self.Initiative = int(line_tok[1])
                elif line_tok[0] == "Speed":
                    self.Speed = int(line_tok[1])
                elif line_tok[0] == "AC":
                    self.AC = int(line_tok[1])
                elif line_tok[0] == "Shield":
                    self.Shield = int(line_tok[1])
                elif line_tok[0] == "Weapon":
                    self.Weapon = weapon(line_tok[1], line_tok[2], line_tok[3], line_tok[4:])
                else:
                    print("Error: Invalid Stat")

    def export_character(self):
        stats = vars(self)
        with open(f"text/{self.Name}.txt", "w") as file:
            for stat in stats:
                if stat == "Weapon":
                    file.write(f"Weapon {self.Weapon.export()}")
                else:
                    file.write(f"{stat} {stats[stat]}\n")

    def create_character(self):
        """
        creates a character object.
        """
        self.Name = input("Enter Character Name: ")
        self.Strength = int(input("Enter Strength: "))
        self.Dexterity = int(input("Enter Dexterity: "))
        self.Constitution = int(input("Enter Constitution: "))
        self.Intelligence = int(input("Enter Intelligence: "))
        self.Wisdom = int(input("Enter Wisdom: "))
        self.Charisma = int(input("Enter Charisma: "))
        self.Hitpoints = int(input("Enter Hitpoints: "))
        self.Proficiency_bonus = int(input("Enter Proficiency_bonus Bonus: "))
        self.Initiative = int(input("Enter Initiative: "))
        self.Speed = int(input("Enter Speed: "))
        self.AC = int(input("Enter AC: "))
        self.Weapon = weapon(input("Enter Weapon Name: "), input("Enter Weapon Attack: "),
                             input("Enter Weapon Damage: "), input("Enter Weapon Crit Range: ").split(","))

    def attack(self):
        """
        makes an attack!
        """
        return self.Weapon.attack()
