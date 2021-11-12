import ddpp
import ddpp_classes

instance = ddpp_classes.Config()
ddpp.tester()
print("Roll from dict: " + str(ddpp.roll_from_list("test", instance.config_file, instance.variables)[0]))
print("Roll fromString: " + str(ddpp.roll_from_string("1d12 +2", instance.variables)))
print("Average from dict: " + str(ddpp.avg_from_list("big", instance.config_file, instance.variables)))
print("Average fom string w/ replace var: " + str(ddpp.avg_from_string("1d1 +[Dexterity]", instance.variables)))
print("Replace Var: " + str(ddpp.roll_from_list("strength_check", instance.config_file, instance.variables)))
ddpp.death_save()




input("Press ENTER to close.")
