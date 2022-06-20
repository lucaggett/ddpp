# *-* coding: utf-8 *-*
# pylint: disable=line-too-long
"""
Unit tests for the ddpp module.
"""
import sys
import time
import unittest
import ddpp
import databases


class DDPPTest(unittest.TestCase):
    """
    Test the dppp module
    """

    def test_s_roll(self):
        """
        test for s_roll
        """
        self.assertEqual(ddpp.Instructions.s_roll(0, 0)[0], 0)
        test_list = []
        print(" ", end="", flush=False)
        start = time.time()
        for i in range(1, 10**6):
            test_list.append(ddpp.Instructions.s_roll(1, 20))
            # print(f"    {i} ", end="\r", flush=True)
        # print(f"\nfinished rolling, took {time.time()-start}")
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
            # print(f"{count }")
            self.assertAlmostEqual(count, avgcount / 20, delta=(avgcount / 20) * 0.02)
            # print(f"{number} was rolled {count} times, devation={count / avgcount}")
        avg = avgsum / avgcount
        deviation = 10.5 - avg
        self.assertLess(abs(deviation), 0.02)
        print("\ns_roll deviation from norm: " + str(deviation) + "\n")

    def test_roll(self):
        """
        test for mult_roll
        """
        self.assertIn(ddpp.Instructions("1d20 +8").roll()[0], range(9, 29))
        self.assertIn(ddpp.Instructions("1d20").roll()[0], range(1, 21))


class DatabaseTest(unittest.TestCase):
    """
    Test the database module
    """

    def test_bestiary(self):
        """
        test for the bestiary database
        """
        database = databases.Bestiary()
        self.assertEqual(len(database.database), 0)
        database.import_source_data()
        self.assertGreater(len(database.database), 0)


if __name__ == "__main__":
    unittest.main()
