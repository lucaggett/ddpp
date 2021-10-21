import ddpp

active = True
instance = ddpp.ddpp()
ddpp.ddpp.importddpp(instance)
while active:
    x = input("input what to roll: ")
    print("Roll = " + str(ddpp.roll_from_string(x, instance.variables)))

