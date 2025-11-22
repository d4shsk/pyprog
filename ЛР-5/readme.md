# Лабораторная работа № 5

## Формулировка задания

Сравните время работы двух реализаций функции вычисления факториала:

1.  Рекурсивной.
2.  Нерекурсивной (итеративной).

Изучить материал про мемоизацию и реализовать сравнение мемоизованных и немемоизованных вариантов функций. Проанализировать результаты, сделать выводы и построить графики зависимости времени выполнения от входных данных.

Для сравнения использовать модуль `timeit`, для визуализации — `matplotlib`.

## Описание работы кода

1.  **Реализация функций:**

      * `fact_rec(n)`: Классическая рекурсия. Имеет накладные расходы на вызов функций и ограничена размером стека.
      * `fact_iter(n)`: Использование цикла `for`. Не расходует память стека, работает линейно.
      * `fact_rec_memo(n)`: Использует декоратор `@lru_cache` из модуля `functools`. При повторных вызовах время выполнения стремится к $O(1)$.
      * `fact_iter_memo(n)`: Использует глобальный словарь `_iter_cache` для хранения результатов.

2.  **Анализ:**

      * Используется список чисел от 1 до 500 с шагом 10.
      * Каждая функция запускается 100 раз (`number=100`) для каждого числа $n$, время усредняется.
      * Модуль `sys` используется для увеличения лимита рекурсии (стандартный Python limit = 1000, что может быть мало для тестов).

## Решение

```python
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
```

## Результат работы программы  

<img width="1489" height="814" alt="image" src="https://github.com/user-attachments/assets/e1083392-98ec-4dde-8e9f-16a2420a8d68" />
  
### Анализ графиков:

1.  Итерация vs Рекурсия:

      * Итеративный метод работает быстрее. График времени растет линейно, но имеет меньший угол наклона. Это связано с тем, что вызов функции в Python — дорогая операция (создание стекового кадра), тогда как цикл оптимизирован.
      * Рекурсивный метод показывает более крутой рост времени выполнения.

2.  Влияние мемоизации:

      * На графике мемоизованные функции (зеленая и красная линии на правом графике) находятся практически на оси X (время близко к 0).
      * Это происходит потому, что мы запускаем вычисление 100 раз подряд. Первый запуск выполняет работу, а следующие 99 мгновенно берут результат из памяти.
      * В среднем время выполнения с мемоизацией на порядки меньше, чем без нее, при условии повторных вызовов.

## Вывод

В ходе лабораторной работы было установлено:

1.  Для задачи вычисления факториала итеративный подход эффективнее рекурсивного в Python из-за отсутствия накладных расходов на управление стеком вызовов.
2.  Мемоизация дает колоссальный прирост производительности при повторных вычислениях одних и тех же значений. Она меняет сложность повторного доступа с $O(N)$ на $O(1)$, однако требует дополнительной памяти для хранения кэша.
