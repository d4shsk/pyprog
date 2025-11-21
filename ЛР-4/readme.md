# Лабораторная работа № 4

## Формулировка задания

Напишите на языке Python нерекурсивную функцию gen_bin_tree, которая будет строить бинарное дерево.  
root = 11, height = 3, left_leaf = root ^ 2, right_leaf = 2 + root ^ 2


## Описание работы кода

1.  **Функция gen_bin_tree**

      * Реализует нерекурсивный подход к построению дерева.
      * Использует список в качестве стека для хранения узлов, которые необходимо обработать.
      * В цикле while извлекает узел, вычисляет значения потомков согласно переданным функциям (left_leaf, right_leaf), создает новые словари и добавляет их обратно в стек.
      * Формирует структуру с ключами value, left, right.

2.  **Функция gen_bin_tree_deque**

      * Альтернативная реализация с использованием модуля collections.
      * Вместо списка использует deque (двустороннюю очередь), что оптимизирует операции добавления и извлечения элементов при построении дерева (подход BFS — обход в ширину).

3.  **Функция print_tree**

      * Вспомогательная функция для рекурсивного вывода структуры дерева в консоль с отступами для наглядности.

## Решение

```python
import collections
from typing import Callable, Dict, Optional, Any
def gen_bin_tree(
        height: int = 3,
        root: float = 11,
        left_leaf: Callable[[float], float] = lambda x: x**2,
        right_leaf: Callable[[float], float] = lambda x: 2 + x**2
) -> Optional[Dict[str, Any]]:
    if height < 0:
        return None

    # Создаем корневой узел
    tree_root = {
        "value": root,
        "left": None,
        "right": None
    }

    # Стек для хранения узлов, которые нужно обработать.
    stack = [(tree_root, height)]

    while stack:
        current_node, current_h = stack.pop()
        # Если мы еще не достигли дна (высота > 0), генерируем потомков
        if current_h > 0:
            val = current_node["value"]
            
            # Вычисляем значения
            l_val = left_leaf(val)
            r_val = right_leaf(val)

            # Создаем новые узлы-словари
            left_node = {"value": l_val, "left": None, "right": None}
            right_node = {"value": r_val, "left": None, "right": None}

            # Привязываем к текущему
            current_node["left"] = left_node
            current_node["right"] = right_node

            # Кладем в стек для следующей итерации (уменьшаем высоту)
            stack.append((left_node, current_h - 1))
            stack.append((right_node, current_h - 1))

    return tree_root

def gen_bin_tree_deque(
        height: int = 3,
        root: float = 11,
        left_leaf: Callable = lambda x: x**2,
        right_leaf: Callable = lambda x: 2 + x**2
) -> Optional[Dict]:
    if height < 0:
        return None

    tree_root = {"value": root, "left": None, "right": None}
    
    # Используем очередь (deque) вместо списка
    queue = collections.deque([(tree_root, height)])

    while queue:
        current_node, current_h = queue.popleft() # Берем первый элемент (FIFO)

        if current_h > 0:
            val = current_node["value"]
            
            left_node = {"value": left_leaf(val), "left": None, "right": None}
            right_node = {"value": right_leaf(val), "left": None, "right": None}

            current_node["left"] = left_node
            current_node["right"] = right_node

            # Добавляем в конец очереди
            queue.append((left_node, current_h - 1))
            queue.append((right_node, current_h - 1))

    return tree_root

def print_tree(tree: Optional[Dict], indent: int = 0):
    """Рекурсивный вывод дерева для визуализации."""
    if tree is None:
        return

    print(" " * indent + f"├── {tree['value']}")
    
    # Проверка, есть ли потомки, чтобы зря не вызывать рекурсию
    if tree.get('left') or tree.get('right'):
        print_tree(tree['left'], indent + 4)
        print_tree(tree['right'], indent + 4)


if __name__ == "__main__":
    print("--- Вариант 1: Базовый (Словарь + Стек) ---")
    # Тест 1: Параметры по умолчанию (из варианта)
    tree_default = gen_bin_tree()
    print_tree(tree_default)

    print("\n--- Вариант 2: Пользовательские параметры ---")
    # Тест 2: Свои параметры
    tree_custom = gen_bin_tree(
        height=2, 
        root=2, 
        left_leaf=lambda x: x + 1, 
        right_leaf=lambda x: x - 1
    )
    print_tree(tree_custom)
    
    print("\n--- Вариант 3: Использование collections.deque ---")
    tree_col = gen_bin_tree_deque(height=2, root=5)
    print_tree(tree_col)
```

## Проверка

Тесты реализованы с помощью модуля unittest. Они проверяют корректность структуры данных, математические вычисления потомков, граничные условия (отрицательная высота) и работу реализации через collections.

**Пояснение к тестам:**

  * test_negative_height: Проверяет, что функция возвращает None при некорректной высоте.
  * test_zero_height: Проверяет создание единственного корневого узла.
  * test_structure_keys: Убеждается, что словарь содержит требуемые ключи (value, left, right).
  * test_default_lambdas: Проверяет математику по умолчанию ($x^2$ и $2+x^2$).
  * test_deque_implementation: Проверяет, что версия с collections.deque выдает идентичный математический результат.

<!-- end list -->

```python
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
```
