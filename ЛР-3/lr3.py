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
