import unittest
from lr3 import gen_bin_tree

class TestBinaryTree(unittest.TestCase):
    def test_tree_1(self):
        tree = gen_bin_tree(height=3, root=5)
        self.assertEqual(tree['root'], 5)

    def test_tree_2(self):
        tree = gen_bin_tree(height=3, root=3)
        self.assertEqual(tree['left']['root'], 9)  # 3^2 = 9

    def test_tree_3(self):
        tree = gen_bin_tree(height=3, root=4)
        self.assertEqual(tree['right']['root'], 18)  # 2 + 4^2 = 18

    def test_tree_4(self):
        tree = gen_bin_tree(height=3, root=2)
        self.assertEqual(tree['left']['left']['root'], 16)  # (2^2)^2 = 16
    
    def test_tree_5(self):
        tree = gen_bin_tree(height=3, root=2)
        self.assertEqual(tree['left']['right']['root'], 18)  # 2 + (2^2)^2 = 18
    
    def test_tree_6(self):
        tree = gen_bin_tree(height=3, root=3)
        self.assertEqual(tree['right']['left']['root'], 121)  # (2 + 3^2)^2 = 121
    
    def test_tree_7(self):
        tree = gen_bin_tree(height=3, root=3)
        self.assertEqual(tree['right']['right']['root'], 123)  # 2 + (2 + 3^2)^2 = 123

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
