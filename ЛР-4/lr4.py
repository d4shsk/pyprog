from typing import Callable, Dict, Optional
from collections import deque

def gen_bin_tree(
        height: int = 3, 
        root: float = 11,
        left_leaf: Callable[[float], float] = lambda x: x**2,
        right_leaf: Callable[[float], float] = lambda x: 2 + x**2
) -> Optional[Dict]:
    if height < 0:
        return None

    # Создаём корневой узел
    tree = {'value': root, 'left': None, 'right': None}
    
    # Используем очередь для построения дерева в ширину
    queue = deque([(tree, 0)])

    while queue:
        node, level = queue.popleft()
        if level < height:
            # Создаём левого и правого потомка
            left_value = left_leaf(node['value'])
            right_value = right_leaf(node['value'])
            
            node['left'] = {'value': left_value, 'left': None, 'right': None}
            node['right'] = {'value': right_value, 'left': None, 'right': None}
            
            # Добавляем потомков в очередь с увеличением уровня
            queue.append((node['left'], level + 1))
            queue.append((node['right'], level + 1))
    
    return tree

def print_tree(tree, indent: int = 0):
    if tree is None:
        return
    print(" " * indent + f"├── {tree['value']}")
    if tree['left'] or tree['right']:
        print_tree(tree['left'], indent + 4)
        print_tree(tree['right'], indent + 4)
