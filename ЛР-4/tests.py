import unittest
from lr4 import gen_bin_tree, gen_bin_tree_deque

class TestBinaryTree(unittest.TestCase):

    def test_negative_height(self):
        """Проверка: при отрицательной высоте возвращается None"""
        tree = gen_bin_tree(height=-1)
        self.assertIsNone(tree, "При высоте < 0 должно возвращаться None")

    def test_zero_height(self):
        """Проверка: при высоте 0 создается только корень без потомков"""
        root_val = 10
        tree = gen_bin_tree(height=0, root=root_val)
        
        self.assertIsNotNone(tree)
        self.assertEqual(tree['value'], root_val)
        self.assertIsNone(tree['left'], "При высоте 0 левый потомок должен быть None")
        self.assertIsNone(tree['right'], "При высоте 0 правый потомок должен быть None")

    def test_default_lambdas_structure(self):
        """Проверка математики по умолчанию (x^2 и 2 + x^2) для высоты 1"""
        # root = 2
        # left = 2^2 = 4
        # right = 2 + 2^2 = 6
        tree = gen_bin_tree(height=1, root=2)

        self.assertEqual(tree['value'], 2)
        
        # Проверяем левого потомка
        self.assertIsNotNone(tree['left'])
        self.assertEqual(tree['left']['value'], 4)
        
        # Проверяем правого потомка
        self.assertIsNotNone(tree['right'])
        self.assertEqual(tree['right']['value'], 6)

    def test_custom_lambdas(self):
        """Проверка передачи пользовательских функций"""
        # left: x + 1
        # right: x - 1
        tree = gen_bin_tree(
            height=1, 
            root=10, 
            left_leaf=lambda x: x + 1, 
            right_leaf=lambda x: x - 1
        )

        self.assertEqual(tree['left']['value'], 11)
        self.assertEqual(tree['right']['value'], 9)

    def test_structure_keys(self):
        """Проверка наличия обязательных ключей в словаре"""
        tree = gen_bin_tree(height=0)
        keys = tree.keys()
        self.assertIn('value', keys)
        self.assertIn('left', keys)
        self.assertIn('right', keys)

    def test_deque_implementation(self):
        """Проверка альтернативной реализации через collections.deque"""
        # Проверяем, что версия с очередью выдает такой же результат математически
        tree = gen_bin_tree_deque(height=1, root=3)
        
        # root = 3
        # left = 3^2 = 9
        # right = 2 + 3^2 = 11
        self.assertEqual(tree['value'], 3)
        self.assertEqual(tree['left']['value'], 9)
        self.assertEqual(tree['right']['value'], 11)

    def test_deep_tree(self):
        """Проверка, что дерево строится на глубину (пример height=2)"""
        tree = gen_bin_tree(height=2, root=2)
        
        # Уровень 0: 2
        # Уровень 1: L=4, R=6
        # Уровень 2 (от L=4): L=16 (4^2)
        
        left_child = tree['left']
        left_grandchild = left_child['left']
        
        self.assertIsNotNone(left_grandchild)
        self.assertEqual(left_grandchild['value'], 16)
        self.assertIsNone(left_grandchild['left'])

if __name__ == '__main__':
    unittest.main()