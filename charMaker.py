def varMaker(variable):
    with open("character.var", "a") as file:
        file.write(variable)

def proMaker(proficiency):
    with open("proficiencies.var", "a") as file:
        file.write(proficiency)


stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

print("Welcome to the Character Maker!")
for stat in stats:
    x = input(f"Please enter your {stat} modifier! :")
    varMaker(f"{stat} {x}\n")
x = input("Please enter your Proficiency Bonus")
varMaker(f"PRO {x}")
x = input("please enter your proficiencies, seperated by spaces : ")
x = x.split(" ")
for proficiency in x:
    proMaker(proficiency)