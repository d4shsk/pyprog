import unittest
from lr4 import gen_bin_tree

class TestBinaryTree(unittest.TestCase):
    def test_root_value(self):
        tree = gen_bin_tree(root=5)
        self.assertEqual(tree['value'], 5)
    
    def test_left_right_values(self):
        tree = gen_bin_tree(root=3)
        self.assertEqual(tree['left']['value'], 9)   # 3^2 = 9
        self.assertEqual(tree['right']['value'], 11) # 2 + 3^2 = 11
    
    def test_left_left_value(self):
        tree = gen_bin_tree(root=2, height=2)
        self.assertEqual(tree['left']['left']['value'], 16)  # 4^2 = 16
    
    def test_right_right_value(self):
        tree = gen_bin_tree(root=2, height=2)
        self.assertEqual(tree['right']['right']['value'], 38)  # 2 + 6^2 = 38
    
    def test_tree_height_0(self):
        tree = gen_bin_tree(root=7, height=0)
        self.assertEqual(tree['value'], 7)
        self.assertIsNone(tree['left'])
        self.assertIsNone(tree['right'])
    
    def test_tree_custom_functions(self):
        # Используем другие функции для потомков
        tree = gen_bin_tree(root=2, left_leaf=lambda x: x+1, right_leaf=lambda x: x+2)
        self.assertEqual(tree['left']['value'], 3)
        self.assertEqual(tree['right']['value'], 4)
        
if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)