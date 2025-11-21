import sys
import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

sys.setrecursionlimit(3000)

# Рекурсивная реализация
def fact_rec(n):
    if n == 0:
        return 1
    return n * fact_rec(n - 1)

# Нерекурсивная (итеративная) реализация 
def fact_iter(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Рекурсивная с мемоизацией
# Используем встроенный декоратор Python для кэширования результатов
@lru_cache(maxsize=None)
def fact_rec_memo(n):
    if n == 0:
        return 1
    return n * fact_rec_memo(n - 1)

# Нерекурсивная с мемоизацией
# Используем словарь для хранения уже вычисленных значений
_iter_cache = {}

def fact_iter_memo(n):
    if n in _iter_cache:
        return _iter_cache[n]
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    _iter_cache[n] = result
    return result

def run_benchmark():
    # Параметры тестирования
    test_values = list(range(1, 500, 10))  # Числа от 1 до 500 с шагом 10
    runs = 100  # Количество запусков для усреднения

    # Списки для сохранения времени
    times_rec = []
    times_iter = []
    times_rec_memo = []
    times_iter_memo = []

    print(f"Запуск бенчмарка для {len(test_values)} значений. Повторений: {runs}...")

    for n in test_values:
        # 1. Рекурсия
        t_rec = timeit.timeit(lambda: fact_rec(n), number=runs)
        times_rec.append(t_rec / runs)

        # 2. Итерация
        t_iter = timeit.timeit(lambda: fact_iter(n), number=runs)
        times_iter.append(t_iter / runs)

        # 3. Рекурсия + Мемоизация
        fact_rec_memo.cache_clear() # Очистим перед серией замеров для данного n
        # Первый вызов заполнит кэш, остальные 99 возьмут из кэша.
        t_rec_m = timeit.timeit(lambda: fact_rec_memo(n), number=runs)
        times_rec_memo.append(t_rec_m / runs)

        # 4. Итерация + Мемоизация
        _iter_cache.clear() # Очистка перед замером
        t_iter_m = timeit.timeit(lambda: fact_iter_memo(n), number=runs)
        times_iter_memo.append(t_iter_m / runs)

    # Построение графиков
    plt.figure(figsize=(12, 6))

    # График 1: Рекурсия vs Итерация (Обычные)
    plt.subplot(1, 2, 1)
    plt.plot(test_values, times_rec, label='Рекурсия', color='red')
    plt.plot(test_values, times_iter, label='Итерация', color='blue')
    plt.title("Обычные реализации")
    plt.xlabel("Число n")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)

    # График 2: Сравнение всех (включая мемоизацию)
    # Мемоизация будет почти на нуле, так как 99 из 100 запусков мгновенные
    plt.subplot(1, 2, 2)
    plt.plot(test_values, times_rec, label='Рекурсия', linestyle='--', alpha=0.5)
    plt.plot(test_values, times_iter, label='Итерация', linestyle='--', alpha=0.5)
    plt.plot(test_values, times_rec_memo, label='Рекурсия (Memo)', linewidth=2)
    plt.plot(test_values, times_iter_memo, label='Итерация (Memo)', linewidth=2)
    plt.title("Сравнение с мемоизацией (с усреднением)")
    plt.xlabel("Число n")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_benchmark()