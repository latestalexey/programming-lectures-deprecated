# coding: utf-8

"""
__Поиск медианы в произвольном массиве__

Материалы: лекция 23.01, семинар 26.01.

Лектор: Объедков Сергей Александрович<br>
Семинарист: Макаров Илья Андреевич<br>
Конспектировал Гончаров Владимир

"""

import random
from sorts import insertion_sort

"""
## `k`-ая порядковая статистика

Пусть у нас есть массив `A`.
\\(k \\)-ая порядковая статистика&nbsp;— это элемент `sorted(A)[k]`.
Соответственно, медиана&nbsp;— `n // 2`-ая порядковая статистика.

Для поиска порядковых статистик существует два алгоритма, оба похожи на qsort.
Различаются они лишь выбором опорного элемента.

Суть:

Выбираем опорный элемент, применяем partition.
Если `k == i = partition(a)`, мы нашли нашу статистику, если нет&nbsp;—
применяем алгоритм к нужной половине, модифицируя k.

    После применения partition:

    |    < p    |p|    > p    |
                 ^
                 i

Если  K < i, запускаем алгоритм на массиве `[0, i)` и ищем `k`-ю статистику.
Если  K > i, запускаем алгоритм на массиве `(i, n)`
и ищем `k - i - 1`-ю статистику.

Этот алгоритм конечен&nbsp;— на каждом шаге мы избавляемся хотябы от одного
элемента, при этом время оценивается также, как у qsort,
за тем лишь исключением, что мы спускаемся лишь по одной ветви рекурсии.
Таким образом получаем худшее время&nbsp;— \\(O(n^2) \\),
среднее&nbsp;— \\(O(n) \\).

"""

#d

"""
## Медиана медиан (Median of Medians, BFPRT)

Меньше, чем за \\(O(n) \\) найти статистику нельзя,
потому что нужно посмотреть каждый элемент.

Хочется стабилизировать наш алгоритм,
чтобы он не деградировал до \\(O(n^2) \\).

Будем на каждом шаге выбирать средний элемент.
Тогда можно будет утверждать, что наша оценка `T[n] = T[n/2] + O(n) = O(n)`.
Но расчитать центральный элемент&nbsp;— это и есть найти медиану,
в неупорядоченном массиве это сложно =) Тогда будем брать элемент,
близкий к медиане.

Для этого поступим следующим образом:

*   Разделим входной массив на части по 5 элементов (получится `n // 5` частей)
*   Каждую отсортируем (так как части имеют фиксированный размер,
    считаем, что сортировка проходит за \\(O(1) \\))
*   Теперь в каждой части выберем медиану и соберем медианы
    в начале массива. На это уйдет \\(O(n) \\) операций.
    То, что осталось в конце массива (если его длинна не кратна 5), оставим.
*   Теперь рекурсивно запустим наш алгоритм на начале массива
    (первые `n // 5` элементов) и найдем-таки элемент,
    составляющий медиану из выбранных ранее медиан (`n // 10`-я статистика).

Заметим теперь, что хотябы 30% элементов в массиве
не больше медианы медиан и 30%&nbsp;— не меньше.

Тогда если выбрать ее в качестве опоры для разделения,
хотябы 30% элементов окажутся левее и хотябы 30%&nbsp;— правее.
Значит в худшем случае время работы алгоритма&nbsp;—
\\(T[n] \le T[n/5] + T[7n/10] + O(n) \\).

Оценим эту формулу. Попробуем понять, верно ли, что она линейная.
Для этого явно выразим \\(O(n) = ln \\), подставим это выражение в
формулу и попробуем найти \\(l \\).

\\(
T[n] \le T[n/5] + T[7n/10] + O(n) \le \\\\
    \le O(n) + \frac 15 \cdot ln + \frac 7{10} \cdot ln
    = O(n) + \frac 9{10} ln = ln
\\)

Видно, что при \\(l = 10 \cdot O(n) = O(n) \\) формула работает.

Таким образом мы получили алгоритм,
ищущий медиану гарантированно за \\(O(n) \\).
Проблема лишь в том, что на практике первый алгоритм с рандомом быстрее.

Подробнее про этот алгоритм можно почитать
[на хабре](http://habrahabr.ru/post/247053/)

P.S. Ели делить не на 5 элементов, будет фейл&nbsp;—
мы не сможем подобрать \\(l \\).

"""
def partition(a, left=0, right=None, pivot_index=None):
    # Не самая удачная реализация, но работает, и ладно.

    if right is None:
        right = len(a)

    if pivot_index is None:
        pivot_index = random.randrange(left, right)

    partitions = []
    j = left
    for i in range(left, right):
        if a[i] < a[pivot_index]:
            if pivot_index == i:
                pivot_index = j
            elif pivot_index == j:
                pivot_index = i
            a[j], a[i] = a[i], a[j]
            j += 1
    partitions.append(j)
    for i in range(j, right):
        if not (a[pivot_index] < a[i]):
            if pivot_index == i:
                pivot_index = j
            elif pivot_index == j:
                pivot_index = i
            a[j], a[i] = a[i], a[j]
            j += 1
    partitions.append(j)

    return partitions

def median_of_medians(a, left=0, right=None, k=None):
    if right is None:
        right = len(a)

    # Нам нужна `k`-я статистика
    if k is None:
        k = (right - left) // 2

    assert left <= right
    if right - left <= 5:
        insertion_sort(a, left, right)
        return left + k

    # Делим все на подмассивы по 5 частей
    blocks = (right - left) // 5
    b, c = left, left
    for i in range(blocks):
        insertion_sort(a, i * 5, i * 5 + 5)
        b += 2
        a[b], a[c] = a[c], a[b]
        c += 1
        b += 3

    pivot_index = median_of_medians(a, left, left + blocks,
                                    blocks // 2)

    i, j = partition(a, left, right, pivot_index)

    size1 = i - left
    size2 = j - i

    if k < size1:
        return median_of_medians(a, left, i, k)
    if k < size1 + size2:
        return i
    return median_of_medians(a, j, right,
                             k - size1 - size2)

if __name__ == '__main__':
    for i in range(100):
        n = random.randint(10, 1000)
        a = list(range(n))

        k = random.randint(0, n - 1)

        expected = a[k]

        random.shuffle(a)

        result = a[median_of_medians(a, k=k)]

        try:
            assert result == expected
        except AssertionError:
            print('Output:', result)
            print('Expected:', expected)
            print('Input:', a)
            raise AssertionError('ERROR! Median of medians is incorrect!')
