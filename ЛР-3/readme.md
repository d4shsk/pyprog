# Лабораторная работа № 3

## Формулировка задания
Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева.

root = 11, height = 3, left_leaf = root ^ 2, right_leaf = 2 + root ^ 2

## Описание работы кода

1. Функция gen_bin_tree  
Генерирует бинарное дерево  
На вход получает высоту и значение корня дерева  
Базовый случай рекурсии: если высота достигла 0, возвращаем None  
Вычисляет значения для левого и правого потомков  
left_leaf = root ^ 2, right_leaf = 2 + root ^ 2  
Возвращает словарь: {'value': root, 'left': gen_bin_tree(height-1, left_leaf), 'right': gen_bin_tree(height-1, right_leaf)}.  

2. Функция print_tree  
На вход получает tree и additional - отступ в пробелах
Базовый случай: если дерево пустое, ничего не делаем  
Сначала печатаем правое поддерево с увеличенным отступом  
Это обеспечивает поворот дерева на 90° против часовой стрелки  
Печатает текущее значение с нужным отступом  
Затем печатает левое поддерево с увеличенным отступом  

## Решение
```Python
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
```
