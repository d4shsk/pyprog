def gen_bin_tree(height=3, root=11):
    if height == 0:
        return None
    left_leaf = root ** 2
    right_leaf = 2 + root ** 2
    return {
        'value': root,
        'left': gen_bin_tree(height - 1, left_leaf),
        'right': gen_bin_tree(height - 1, right_leaf)
    }

def print_tree(tree, additional=0):
    if tree is None:
        return None
    print_tree(tree['right'], additional + 4)
    print(' ' * additional + f"{tree['value']}")
    print_tree(tree['left'], additional + 4)

tree = gen_bin_tree()
print_tree(tree)