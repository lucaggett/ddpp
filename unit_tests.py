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
        test_char.Strength = 10
        test_char.Dexterity = 10
        test_char.Constitution = 10
        test_char.Intelligence = 10
        test_char.Wisdom = 10
        test_char.Charisma = 10
        test_char.Speed = 10
        test_char.Initiative = 10
        test_char.Name = "Test"
        test_char.AC = 10
        test_char.Weapon = ddpp_classes.weapon("test", "1d10", "1d20", [19, 20])
        test_char.export_character()
        self.assertIsInstance(test_char.Name, str)
        self.assertIsInstance(test_char.Strength, int)
        self.assertIsInstance(test_char.Dexterity, int)
        self.assertIsInstance(test_char.Constitution, int)
        self.assertIsInstance(test_char.Intelligence, int)
        self.assertIsInstance(test_char.Wisdom, int)
        self.assertIsInstance(test_char.Charisma, int)
        self.assertIsInstance(test_char.Hitpoints, int)
        self.assertIsInstance(test_char.AC, int)
        self.assertIsInstance(test_char.Initiative, int)
        self.assertIsInstance(test_char.Speed, int)
        self.assertIsInstance(test_char.Proficiency_bonus, int)
        self.assertIsInstance(test_char.Weapon, ddpp_classes.weapon)
        import_test = ddpp_classes.character()
        import_test.import_char("text/Test.txt")
        self.assertEqual(test_char.Name, import_test.Name)
        self.assertEqual(test_char.Strength, import_test.Strength)
        self.assertEqual(test_char.Dexterity, import_test.Dexterity)
        self.assertEqual(test_char.Constitution, import_test.Constitution)
        self.assertEqual(test_char.Intelligence, import_test.Intelligence)
        self.assertEqual(test_char.Wisdom, import_test.Wisdom)
        self.assertEqual(test_char.Charisma, import_test.Charisma)
        self.assertEqual(test_char.Hitpoints, import_test.Hitpoints)
        self.assertEqual(test_char.AC, import_test.AC)
        self.assertEqual(test_char.Initiative, import_test.Initiative)
        self.assertEqual(test_char.Speed, import_test.Speed)
        self.assertEqual(test_char.Proficiency_bonus, import_test.Proficiency_bonus)
        self.assertEqual(test_char.Weapon.name, import_test.Weapon.name)
        self.assertEqual(test_char.Weapon.damage, import_test.Weapon.damage)
        self.assertEqual(test_char.Weapon.crit_range, import_test.Weapon.crit_range)





if __name__ == '__main__':
    unittest.main()
