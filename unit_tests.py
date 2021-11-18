# *-* coding: utf-8 *-*
# pylint: disable=line-too-long
"""
Unit tests for the ddpp module.
"""
import sys
import time
import unittest
import ddpp
import ddpp_classes


class DDPPTest(unittest.TestCase):
    """
    Test the dppp module
    """

    def test_s_roll(self):
        """
        test for s_roll
        """
        self.assertEqual(ddpp.s_roll(0, 0)[0], 0)
        test_list = []
        print(" ", end="", flush=False)
        start = time.time()
        for i in range(1, 10**6):
            test_list.append(ddpp.s_roll(1, 20))
            print(f"    {i} ", end="\r", flush=True)
        print(f"\nfinished rolling, took {time.time()-start}")
        avgsum = 0
        avgcount = 0
        distdict = {}
        for number, _ in test_list:
            self.assertTrue(number <= 20)
            self.assertTrue(number >= 1)
            avgsum += number
            avgcount += 1
        for number, _ in test_list:
            if number in distdict:
                distdict[number] += 1
            else:
                distdict.update({number: 0})
        for number, count in sorted(distdict.items()):
            #print(f"{count }")
            self.assertAlmostEqual(count, avgcount / 20, delta=(avgcount / 20)*0.01)
            #print(f"{number} was rolled {count} times, devation={count / avgcount}")
        avg = avgsum / avgcount
        deviation = 11 - avg
        self.assertLess(abs(deviation), 0.5)
        print("\ns_roll deviation from norm: " + str(deviation) + "\n")

    def test_mult_roll(self):
        """
        test for mult_roll
        """
        self.assertIsInstance(ddpp.mult_roll(["1d20", "+8"]), tuple)
        self.assertIsInstance(ddpp.mult_roll(["1d20, +8, -9"]), tuple)

    def test_mult_avg(self):
        """
        test for mult_avg
        Should propably add more tests
        """
        self.assertTrue(ddpp.mult_avg(["1d20", "+8"]) == 18.5)
        self.assertTrue(ddpp.mult_avg(["1d20", "+8", "-9"]) == 9.5)

    def test_s_avg(self):
        """
        test for s_avg
        """
        self.assertTrue(ddpp.s_avg(1, 20) == 10.5)
        self.assertTrue(ddpp.s_avg(1, 12) == 6.5)


class ClassesTest(unittest.TestCase):
    """
    unit tests for ddpp_classes.py
    """

    def test_character(self):
        """
        test for the Character class
        """
        test_char = ddpp_classes.Character()
        test_char.strength = 10
        test_char.dexterity = 10
        test_char.constitution = 10
        test_char.intelligence = 10
        test_char.wisdom = 10
        test_char.charisma = 10
        test_char.speed = 10
        test_char.initiative = 10
        test_char.name = "Test"
        test_char.armor_class = 10
        test_char.weapon = ddpp_classes.Weapon("test", "1d10", "1d20", [19, 20])
        test_char.export_character()
        self.assertIsInstance(test_char.name, str)
        self.assertIsInstance(test_char.strength, int)
        self.assertIsInstance(test_char.dexterity, int)
        self.assertIsInstance(test_char.constitution, int)
        self.assertIsInstance(test_char.intelligence, int)
        self.assertIsInstance(test_char.wisdom, int)
        self.assertIsInstance(test_char.charisma, int)
        self.assertIsInstance(test_char.health_points, int)
        self.assertIsInstance(test_char.armor_class, int)
        self.assertIsInstance(test_char.initiative, int)
        self.assertIsInstance(test_char.speed, int)
        self.assertIsInstance(test_char.proficiency, int)
        self.assertIsInstance(test_char.weapon, ddpp_classes.Weapon)
        import_test = ddpp_classes.Character()
        import_test.import_char("text/Test.txt")
        print(import_test.name)
        self.assertEqual(test_char.name, import_test.name)
        self.assertEqual(test_char.strength, import_test.strength)
        self.assertEqual(test_char.dexterity, import_test.dexterity)
        self.assertEqual(test_char.constitution, import_test.constitution)
        self.assertEqual(test_char.intelligence, import_test.intelligence)
        self.assertEqual(test_char.wisdom, import_test.wisdom)
        self.assertEqual(test_char.charisma, import_test.charisma)
        self.assertEqual(test_char.health_points, import_test.health_points)
        self.assertEqual(test_char.armor_class, import_test.armor_class)
        self.assertEqual(test_char.initiative, import_test.initiative)
        self.assertEqual(test_char.speed, import_test.speed)
        self.assertEqual(test_char.proficiency, import_test.proficiency)
        self.assertEqual(test_char.weapon.name, import_test.weapon.name)
        self.assertEqual(test_char.weapon.damage, import_test.weapon.damage)
        self.assertEqual(test_char.weapon.crit_range, import_test.weapon.crit_range)

    def test_weapon(self):
        """
        tests for the Weapon class in ddpp.py, mainly for the export and attack_roll functions
        """
        test_weapon = ddpp_classes.Weapon("test", "1d10", "1d20", [19, 20])
        self.assertTrue(test_weapon.export() == "test 1d10 1d20 19 20")
        attack = test_weapon.attack_roll()
        self.assertIsInstance(attack, tuple)
        self.assertIsInstance(attack[0], int)
        self.assertIsInstance(attack[1], str)
        self.assertIsInstance(attack[2], int)
        self.assertIsInstance(attack[3], str)


if __name__ == "__main__":
    unittest.main()
