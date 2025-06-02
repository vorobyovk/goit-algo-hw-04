import timeit
import random
import matplotlib.pyplot as plt
import pandas as pd
import math

# --- Реалізації алгоритмів сортування ---
def insertion_sort(arr_input):
    """Сортування вставками. Повертає новий відсортований список."""
    arr = list(arr_input) # Робота з копією
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr_input):
    """Сортування злиттям. Повертає новий відсортований список."""
    arr = list(arr_input) # Робота з копією
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        # Рекурсивно сортуємо обидві половини
        L_sorted = merge_sort(L)
        R_sorted = merge_sort(R)

        # Зливаємо відсортовані половини
        i = j = k = 0
        while i < len(L_sorted) and j < len(R_sorted):
            if L_sorted[i] < R_sorted[j]:
                arr[k] = L_sorted[i]
                i += 1
            else:
                arr[k] = R_sorted[j]
                j += 1
            k += 1

        while i < len(L_sorted):
            arr[k] = L_sorted[i]
            i += 1
            k += 1

        while j < len(R_sorted):
            arr[k] = R_sorted[j]
            j += 1
            k += 1
    return arr

# --- Функції генерації даних ---
def create_random_list(size, max_val=None):
    if max_val is None:
        max_val = size * 10
    return [random.randint(0, max_val) for _ in range(size)]

def create_sorted_list(size):
    return list(range(size))

def create_reverse_sorted_list(size):
    return list(range(size, 0, -1))

def create_list_with_few_unique(size, unique_ratio=0.05):
    num_unique = max(1, int(size * unique_ratio))
    # Обмежимо кількість унікальних значень, щоб уникнути надто великих чисел, якщо size * unique_ratio дуже малий
    if num_unique < 2 and size > 10 : # Ensure some repetition if size is not tiny
        num_unique = max(2,min(5, size //2))
    pool = [random.randint(0, num_unique * 5) for _ in range(num_unique)]
    if not pool: # Ensure pool is not empty for size 0 or 1 if num_unique became 0
        pool = [0]
    return [random.choice(pool) for _ in range(size)]

# --- Логіка тестування та збору результатів ---
results = []

algorithms_to_test = {
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Timsort (sorted())": sorted
}

# Розміри списків для тестування
list_sizes = [10, 50, 100, 200, 500, 1000, 2500] 

# Типи списків
list_types_generators = {
    "Випадковий": create_random_list,
    "Відсортований": create_sorted_list,
    "Зворотно відсортований": create_reverse_sorted_list,
    "З малою кількістю унікальних значень": create_list_with_few_unique
}

print("Запуск тестування продуктивності сортування...")

for type_name, generator_func in list_types_generators.items():
    print(f"\nТестування типу списку: {type_name}")
    for size in list_sizes:
        test_list = generator_func(size)
        # Для списків розміром 0 або 1, деякі генератори можуть дати порожні або специфічні списки.
        # Сортування таких списків дуже швидке, але це крайні випадки.
        if not test_list and size > 0: # Avoid issues if generator returns empty for non-zero size
            print(f"  Пропуск розміру {size} для {type_name} через порожній згенерований список.")
            continue
        for algo_name, algo_func in algorithms_to_test.items():
            # Обмеження для сортування вставками на великих масивах
            if algo_name == "Insertion Sort" and size > 2500:
                time_taken = float('inf') # Позначимо як нескінченність для графіків
            else:
                # Динамічне визначення кількості запусків для timeit
                if size <= 100:
                    timeit_number = 100
                elif size <= 500:
                    timeit_number = 20
                elif size <= 1000:
                    timeit_number = 5
                else: # size > 1000
                    timeit_number = 2

                if algo_name == "Insertion Sort":
                    if size <= 100: timeit_number = 50
                    elif size <= 200: timeit_number = 20
                    elif size <= 500: timeit_number = 5
                    elif size <= 1000: timeit_number = 2
                    else: timeit_number = 1 
                timeit_repeat = 3
                
                # Використання timeit.repeat для отримання списку загальних часів
                # stmt виконується `timeit_number` разів. Цей блок повторюється `timeit_repeat` разів.
                try:
                    times = timeit.repeat(
                        stmt='algo_func_timed(data_timed)',
                        setup='pass', # Глобальні змінні передаються через globals
                        globals={'algo_func_timed': algo_func, 'data_timed': test_list},
                        number=timeit_number,
                        repeat=timeit_repeat
                    )
                    # min_total_time - це мінімальний час для `timeit_number` виконань
                    # Отже, середній час одного виконання - min_total_time / timeit_number
                    time_taken = min(times) / timeit_number
                except Exception as e:
                    print(f"Помилка під час тестування {algo_name} з розміром {size} для типу {type_name}: {e}")
                    time_taken = float('nan') # Not a Number, щоб позначити помилку

            results.append({
                'Algorithm': algo_name,
                'List Type': type_name,
                'Size': size,
                'Time': time_taken
            })
            if math.isfinite(time_taken):
                 print(f"  {algo_name} | Розмір: {size:<5} | Час: {time_taken:.6f} сек")
            elif math.isinf(time_taken):
                 print(f"  {algo_name} | Розмір: {size:<5} | Час: пропущено (занадто довго)")
            else:
                 print(f"  {algo_name} | Розмір: {size:<5} | Час: помилка вимірювання")


print("\nТестування завершено. Генерація графіків...")
# --- Візуалізація результатів ---
df_results = pd.DataFrame(results)
plot_files = []

# Побудова графіків для кожного типу списку
for list_type_name in list_types_generators.keys():
    plt.figure(figsize=(12, 7))
    subset_df = df_results[df_results['List Type'] == list_type_name].copy() # Робота з копією
    
    # Перетворення часу на числовий тип, обробка inf та nan
    subset_df['Time'] = pd.to_numeric(subset_df['Time'], errors='coerce')

    for algo_name in algorithms_to_test.keys():
        algo_df = subset_df[subset_df['Algorithm'] == algo_name].sort_values(by='Size')
        # Відфільтруємо нескінченні та NaN значення для коректного відображення
        algo_df_plot = algo_df.dropna(subset=['Time'])
        algo_df_plot = algo_df_plot[~algo_df_plot['Time'].isin([float('inf'), float('-inf')])]

        if not algo_df_plot.empty:
            plt.plot(algo_df_plot['Size'], algo_df_plot['Time'], marker='o', linestyle='-', label=algo_name)

    plt.xlabel("Розмір списку (N)")
    plt.ylabel("Час виконання (секунди)")
    plt.title(f"Продуктивність сортування: {list_type_name}", fontsize=15)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    # Використання логарифмічної шкали для кращої візуалізації великих діапазонів
    # Перевірка, чи є дані перед встановленням логарифмічної шкали
    if not subset_df.dropna(subset=['Time'])['Time'].empty and (subset_df.dropna(subset=['Time'])['Time'] > 0).any():
        plt.yscale('log')
    if not subset_df.dropna(subset=['Size'])['Size'].empty and (subset_df.dropna(subset=['Size'])['Size'] > 0).any():
        plt.xscale('log')

    # Генерація графіків
    plt.show() # Показати графік перед збереженням
    plt.close() # Закрити графік, щоб звільнити пам'ять

print("\nУсі графіки згенеровано.")