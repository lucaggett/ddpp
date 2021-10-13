def varMaker(variable):
    with open("character.var", "a") as file:
        file.write(variable)


x = input("Welcome to the Character Maker! \nPlease enter your strength modifier! :")
varMaker(f"STR {x}\n")
x = input("Please enter your dexterity modifier! : ")
varMaker(f"DEX {x}\n")
x = input("Please enter your constitution modifier! : ")
varMaker(f"CON {x}\n")
x = input("Please enter your intelligence modifier! : ")
varMaker(f"INT {x}\n")
x = input("Please enter your wisdom modifier! : ")
varMaker(f"WIS {x}\n")
x = input("Please enter your charisma modifier! : ")
varMaker(f"CHA {x}\n")

