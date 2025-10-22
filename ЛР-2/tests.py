import unittest
from lr2 import sum

class TestMath(unittest.TestCase):
    def test_sum_1(self):
        self.assertEqual(sum([2, 7, 11, 15], 9), [0, 1])
        
    def test_sum_2(self):
        self.assertEqual(sum([3, 2, 4], 6), [1, 2])

    def test_sum_3(self):
        self.assertEqual(sum([3, 3], 6), [0, 1])

    def test_sum_4(self):
        self.assertEqual(sum([1, 2, 3], 10), [])

    def test_sum_5(self):
        self.assertEqual(sum([-1, -2, -3, 4], 1), [2, 3])

    def test_sum_6(self):
        self.assertEqual(sum([1, 2, 2, 3], 4), [0, 3])

unittest.main(argv=[''], verbosity=2, exit=False)
