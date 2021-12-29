from ddpp_classes import Character


class Fighter(Character):
    def __init__(self):
        super().__init__()
        self.hit_die = 10
        self.proficiencies.append('light armor')
        self.proficiencies.append('medium armor')
        self.proficiencies.append('heavy armor')
        self.proficiencies.append('shields')
        self.proficiencies.append('simple weapons')
        self.proficiencies.append('martial weapons')
        self.saving_throws.append('strength')
        self.saving_throws.append('constitution')
        self.skills.append('athletics')
        self.skills.append('intimidation')
        self.skills.append('strength')
        self.skills.append('survival')

    def __str__(self):
        return 'Fighter'

    def __repr__(self):
        return 'Fighter'

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())


class Paladin(Character):
    def __init__(self):
        super().__init__()
        self.hit_die = 10
        self.proficiencies.append('light armor')
        self.proficiencies.append('medium armor')
        self.proficiencies.append('heavy armor')
        self.proficiencies.append('shields')
        self.proficiencies.append('simple weapons')
        self.proficiencies.append('martial weapons')
        self.saving_throws.append('wisdom')
        self.saving_throws.append('charisma')
        self.skills.append('athletics')
        self.skills.append('insight')
        self.skills.append('intimidation')
        self.skills.append('medicine')
        self.skills.append('persuasion')
        self.skills.append('religion')


class Ranger(Character):
    def __init__(self):
        super().__init__()
        self.hit_die = 10
        self.proficiencies.append('light armor')
        self.proficiencies.append('medium armor')
        self.proficiencies.append('heavy armor')
        self.proficiencies.append('shields')
        self.proficiencies.append('simple weapons')
        self.proficiencies.append('martial weapons')
        self.saving_throws.append('dexterity')
        self.saving_throws.append('wisdom')
        self.skills.append('athletics')
        self.skills.append('insight')
        self.skills.append('investigation')
        self.skills.append('nature')
        self.skills.append('perception')
        self.skills.append('stealth')
