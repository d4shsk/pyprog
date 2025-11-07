# Лабораторная работа № 3

## Формулировка задания
Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева.

root = 11, height = 3, left_leaf = root ^ 2, right_leaf = 2 + root ^ 2

## Описание работы кода

1. Функция gen_bin_tree  
Генерирует бинарное дерево  
Базовый случай рекурсии: если высота достигла 0, возвращаем None  
Вычисляет значения для левого и правого потомков  
Возвращает словарь: tree.  

2. Функция print_tree  
На вход получает tree и indient - отступ в пробелах
Базовый случай: если дерево пустое, ничего не делаем  
Сначала выводит значение текущего узла с отступом
Если есть поддеревья, вызывает функцию рекурсивно для каждого из них

## Решение
```Python
from typing import Callable, Dict, Optional

def gen_bin_tree(
        height: int = 3, 
        root: float = 11,
        left_val: Callable = lambda x: x**2,
        right_val: Callable = lambda x: 2 + x ** 2
) -> Optional[Dict]:
    
    if height < 0:
        return None
    
    tree = {
        'root': root,
        'left': None,
        'right': None
    }

    if height > 0:
        left_value = left_val(root)
        right_value = right_val(root)
        tree['left'] = gen_bin_tree(height - 1, left_value, left_val, right_val)
        tree['right'] = gen_bin_tree(height - 1, right_value, left_val, right_val)

    return tree


def print_tree(tree, indent: int = 0):
    """Рекурсивный вывод бинарного дерева в консоль."""
    if tree is None:
        return

    print(" " * indent + f"├── {tree['root']}")
    if tree['left'] is not None or tree['right'] is not None:
        print_tree(tree['left'], indent + 4)
        print_tree(tree['right'], indent + 4)


if __name__ == "__main__":
    tree = gen_bin_tree()
    print_tree(tree)
```
## Проверка
Тесты реализованы с помощью модуля unittest.
```Python
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
```
