import unittest
import ddpp
import ddpp_classes


class dpppTest(unittest.TestCase):
    # unit tests for ddpp.py
    def test_s_roll(self):
        # test for s_roll
        self.assertEqual(ddpp.s_roll(0, 0), 0)
        test_list = []
        for i in range(1, 100000):
            test_list.append(ddpp.s_roll(1, 20))
        avgsum = 0
        avgcount = 0
        for number in test_list:
            self.assertTrue(number <= 20)
            self.assertTrue(number >= 1)
            avgsum += number
            avgcount += 1
        avg = avgsum / avgcount
        deviation = 11 - avg
        self.assertLess(abs(deviation), 4)
        print("s_roll deviation from norm: " + str(deviation))

    def test_mult_roll(self):
        # test for mult_roll
        self.assertIsInstance(ddpp.mult_roll(["1d20", "+8"]), tuple)
        self.assertIsInstance(ddpp.mult_roll(["1d20, +8, -9"]), tuple)


    def test_mult_avg(self):
        # test for mult_avg
        self.assertTrue(ddpp.mult_avg(["1d20", "+8"]) == 19)
        self.assertTrue(ddpp.mult_avg(["1d20, +8, -9"]) == 10)
        self.assertTrue(ddpp.mult_avg(["1d1"]) == 1)
        self.assertTrue(ddpp.mult_avg(["1d1 1d1"]) == 2)


    def test_roll_from_list(self):
        c = ddpp_classes.config()
        c.import_config()



class classes_test(unittest.TestCase):
    # unit tests for ddpp_classes.py
    def test_character(self):
        # test for character()
        test_char = ddpp_classes.character()
        test_char.strength = 10
        test_char.dexterity = 10
        test_char.constitution = 10
        test_char.intelligence = 10
        test_char.wisdom = 10
        test_char.charisma = 10
        test_char.speed = 10
        test_char.initiative = 10
        test_char.name = "Test"
        test_char.AC = 10
        test_char.weapon = ddpp_classes.weapon("test", "1d10", "1d20", [19, 20])
        test_char.export_character()
        self.assertIsInstance(test_char.name, str)
        self.assertIsInstance(test_char.strength, int)
        self.assertIsInstance(test_char.dexterity, int)
        self.assertIsInstance(test_char.constitution, int)
        self.assertIsInstance(test_char.intelligence, int)
        self.assertIsInstance(test_char.wisdom, int)
        self.assertIsInstance(test_char.charisma, int)
        self.assertIsInstance(test_char.HP, int)
        self.assertIsInstance(test_char.AC, int)
        self.assertIsInstance(test_char.initiative, int)
        self.assertIsInstance(test_char.speed, int)
        self.assertIsInstance(test_char.proficiency, int)
        self.assertIsInstance(test_char.weapon, ddpp_classes.weapon)
        import_test = ddpp_classes.character()
        import_test.import_char("text/Test.txt")
        self.assertEqual(test_char.name, import_test.name)
        self.assertEqual(test_char.strength, import_test.strength)
        self.assertEqual(test_char.dexterity, import_test.dexterity)
        self.assertEqual(test_char.constitution, import_test.constitution)
        self.assertEqual(test_char.intelligence, import_test.intelligence)
        self.assertEqual(test_char.wisdom, import_test.wisdom)
        self.assertEqual(test_char.charisma, import_test.charisma)
        self.assertEqual(test_char.HP, import_test.HP)
        self.assertEqual(test_char.AC, import_test.AC)
        self.assertEqual(test_char.initiative, import_test.initiative)
        self.assertEqual(test_char.speed, import_test.speed)
        self.assertEqual(test_char.proficiency, import_test.proficiency)
        self.assertEqual(test_char.weapon.name, import_test.weapon.name)
        self.assertEqual(test_char.weapon.damage, import_test.weapon.damage)
        self.assertEqual(test_char.weapon.crit_range, import_test.weapon.crit_range)





if __name__ == '__main__':
    unittest.main()
