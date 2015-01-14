# coding: utf-8

"""
__Лекция 1: Оценка сложности алгоритмов, простейшие сортировки__

Рассмотрены простейшие сортировки. К сожалению, пока только код, теорию допишу
позже.

"""

import random
from copy import deepcopy

a = list(range(100))
random.shuffle(a)


def insertion_sort(a):
    """
    ## Сортировка вставками (insertion sort)

    Устойчивая сортировка, эффективная на небольших объемах данных.

    На каждом шаге элемент перемещается назад по массиву до тех пор, пока
    перед ним находится больший элемент.

    «Данный алгоритм можно ускорить при помощи использования
    бинарного поиска для нахождения места текущему элементу в
    отсортированной части. Проблема с долгим сдвигом массива вправо
    решается при помощи смены указателей» — Википедия

    __Время работы:__

    \\(O(n^2) \\) в худшем случае: входной массив отсортирован в порядке,
    обратном нужному.

    \\(O(n) \\) в лучшем: массив уже отсортирован.

    """
    for i in range(1, len(a)):
        key = a[i]
        for k in range(i - 1, -1, -1):
            if key < a[k]:
                a[k], a[k + 1] = a[k + 1], a[k]
            else:
                break
    return a


def merge_sort(a):
    """
    ## Сортировка слиянием (merge sort)

    Алгоритм рекурсивный: на каждом шаге мы разделяем массив
    на две части и сортируем каждую отдельно (тем же самым алгоритмом),
    после чего сливаем две части вместе.

    __Время работы__ \\(O(n \log n) \\).

    Если время работы алгоритма на массиве длинны \\(n \\) — \\(T[n] \\),
    то по определению справедливо рекуррентное соотношение
    \\(T[n] = 2T[n/2] + O(n) \\): две сортировки массивов размера
    \\(n/2 \\) и еще n операций на слияние.

    Можно убедиться, что \\(T[n] = O(n \log n) \\), используя
    [основную теорему о рекуррентных соотношениях][1].

    [1]: https://ru.wikipedia.org/wiki/Основная_теорема_о_рекуррентных_соотношениях

    """
    if len(a) <= 1:
        return a
    else:
        # Стоит отслеживать глубину рекурсии и при необходимости
        # сортировать части массива другим алгоритмом.
        x = merge_sort(a[:len(a) // 2])
        y = merge_sort(a[len(a) // 2:])

        result = []
        i, j = 0, 0
        while i < len(x) and j < len(y):
            if x[i] > y[j]:
                result.append(y[j])
                j += 1
            else:
                result.append(x[i])
                i += 1
        result += x[i:]
        result += y[j:]
        return result


assert (insertion_sort(deepcopy(a)) ==
        merge_sort(deepcopy(a)) ==
        list(range(100)))
