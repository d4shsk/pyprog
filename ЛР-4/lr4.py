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