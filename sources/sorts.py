# coding: utf-8

"""
__Cортировки__

Материалы: лекция 13.01, 16.05, семинар 2 15.01.

Лектор: Объедков Сергей Александрович<br>
Семинарист: Макаров Илья Андреевич<br>
Конспектировал Гончаров Владимир

"""

import random
import tests


"""
## Сортировка выбором (selection sort)

В представлении не нуждается, работает за \\(O(n^2) \\),
есть стабильный вариант.

"""
def selection_sort(a):
    # Нестабильный вариант
    # Обратите внимание, что эта функция является
    # модификативной (in place) и использует O(1) дополнительной памяти.
    i = len(a)
    while i > 1:
        maximum = 0
        for j in range(i):
            if a[j] > a[maximum]:
                maximum = j
        a[i - 1], a[maximum] = a[maximum], a[i - 1]
        i -= 1
    return a

#d

"""
## Сортировка вставками (insertion sort)

Устойчивая сортировка, эффективная на небольших объемах данных.

На каждом шаге элемент перемещается назад по массиву до тех пор, пока
перед ним находится больший элемент. Таким образом у нас есть
начало массива, отсортированное на предыдущих шагах и элемент
на \\(i \\)-м месте, который нужно поместить в отсортированную часть так,
чтобы она осталась отсортированной.

«Данный алгоритм можно ускорить при помощи использования
бинарного поиска для нахождения места текущему элементу в
отсортированной части. Проблема с долгим сдвигом массива вправо
решается при помощи смены указателей»&nbsp;— Википедия

__Время работы:__

\\(O(n^2) \\) в худшем случае: входной массив отсортирован в порядке,
обратном нужному, на каждом участке цикла по \\(i \\) происходит
\\(i \\) операций в цикле по \\(k \\).

\\(O(n) \\) в лучшем: массив уже отсортирован,
на каждом участке цикла по \\(i \\) происходит \\( O(1)\\) операций.

"""
def insertion_sort(a, left=0, right=None):
    if right is None:
        right = len(a)
    # Как и `selection_sort`, in place функция
    # использует O(1) дополнительной памяти.
    for i in range(left + 1, right):
        key = a[i]
        for j in range(i - 1, left - 1, -1):
            if key < a[j]:
                a[j], a[j + 1] = a[j + 1], a[j]
            else:
                break
    return a

#d

"""
## Сортировка слиянием (merge sort)

Алгоритм рекурсивный: на каждом шаге мы разделяем массив
на две части и сортируем каждую отдельно (тем же самым алгоритмом),
после чего сливаем две части вместе.

__Время работы__ \\(O(n \log n) \\).

По определению справедливо рекуррентное соотношение
\\(T[n] = 2T[n/2] + O(n) \\): две сортировки массивов размера
\\(n/2 \\) и еще n операций на слияние.

Можно убедиться, что \\(T[n] = O(n \log n) \\), используя
[основную теорему о рекуррентных соотношениях][1]
(см. [[sorts_theory.py#section-5]]).

[1]: https://ru.wikipedia.org/wiki/Основная_теорема_о_рекуррентных_соотношениях

"""
def merge_sort(a):
    result = []
    if len(a) <= 20:
        # Часто insertion_sort показывает лучшие результаты
        # на небольших массивах.
        return insertion_sort(a)
    else:
        x = merge_sort(a[:len(a) // 2])
        y = merge_sort(a[len(a) // 2:])

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

#d

"""
## Быстрая сортировка (qsort)

Алгоритм быстрой сортировки&nbsp;— объединение идеи пузырьковой сортировки
и сортировки слиянием.

На каждом шаге мы выбираем «опорный элемент» («pivot element»),
после чего переносим все элементы, меньшие опорного,&nbsp;— налево,
большие&nbsp;— направо. После этого мы запускаем сортировку на левой
и правой части массива (центральную не трогаем). Заметим, что после
этой операции не нужно проводить слияние.

__Опорный элемент:__

Выбор опорного элемента напрямую влияет на скорость алгоритма:
самым оптимальным выбором будет медиана, самым худшим&nbsp;—
выбор наименьшего или наибольшего элемента. Так как искать медиану
без дополнительных элементов сложно, используют разные ухищрения:
средний из максимального и минимального элемента, случайный элемент,
медиана из первого, среднего и последнего элемента и т. д.

__Время работы:__

В in place реализации выполняется в среднем за \\(O(n \log n) \\).

При этом в худшем случае, когда в качестве опорного элемента
выбирается минимальный или максимальный элемент,
на каждом шаге мы имеем деление массива
на отрезки [0] и [1, n) за \\(n - 1 \\) операцию обмена,
что ухудшает время до \\(O(n^2) \\).

__Средний случай подробнее:__

Средний, то есть «удачный» случай разделения — случай, когда
опорный элемент близок к медиане. Если предположить, что он
попадает в центральную чать массива (т. е. отстоит от медианы не более,
чем на \\(0{,}25n \\), вероятность чего составит 50% при случайном выборе элемента),
глубина рекурсии составит не более, чем \\(\log_{4/3} n\\), и поскольку
на каждом уровне рекурсии выполняется \\(n \\) операций, мы получаем оценку в
\\(O(n \log n) \\).

__Глубина рекурсии:__

В худшем случае глубина рекурсии составляет \\(O(n) \\).
Существует несколько выходов из ситуации. В их числе:

*   Переход на другой вид сортировки при привышении лимита глубины
    (см. [introsort](https://ru.wikipedia.org/wiki/Introsort))
*   Перестройка алгоритма с использованием хвостовой рекурсии:
    сортировать две полученные части массива в рамках одного вызова.
    К примеру, вместо `left` и `right` передавать список вида
    `[[left, middle], [middle, right]]` и сортировать отрезки в одном цикле.

"""
def quick_sort_inplace(a, left=0, right=None):
    if right is None:
        right = len(a)

    if left < right - 1:
        i, j = left, right - 1

        # В качестве опорного элемента выбирается случайный.
        pivot = random.choice(a[i:j])

        while i <= j:
            while a[i] < pivot:
                i += 1
            while a[j] > pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1

        quick_sort_inplace(a, left, j + 1)
        quick_sort_inplace(a, i, right)

    return a


def quick_sort(a):
    # Пример реализации с использованием списковых сборок.
    # Красиво, компактно, но памяти используется больше.
    if len(a) <= 1:
        return a
    else:
        pivot = random.choice(a)
        return (quick_sort([x for x in a if x < pivot]) +
                [pivot] * a.count(pivot) +
                quick_sort([x for x in a if x > pivot]))

#d

"""
## Сортировка кучей (heap sort, пирамидальная сортировка)

Как известно, идеально сбалансированное бинарное дерево
может быть записано в массив размера \\(n \\).
Heap sort использует бинарное сортирующее дерево, свойства которого
таковы: каждый родитель не меньше своего потомка.

Алгоритм сначала строит на базе массива сортирующее дерево,
а потом, собственно, сортирует.

Анимация всего процесса
[на youtube](http://www.youtube.com/watch?v=R6x7OuF_dYM#t=11)
(качество плохое, но лучше я не нашел).

Часть 1: Построение кучи. Начиная с конца предпоследнего уровня
двигаемся к началу, на каждом шаге пытаясь «протолкнуть» элемент ниже:
если больший потомок меньше родителя, меняем их местами,
и так спускаемся в кучу до тех пор, пока не обнаружим, что оба
потомка больше родителя или что дальше двигаться нельзя (нижний уровень).
В результате этих операций наибольший элемент окажется наверху.

Часть 2: Меняем местами наибольший элемент с последним. Его больше трогать
не нужно, он на своем месте. Теперь наибольший стоит в конце,
а тот, что стоит в корне мы пропихиваем вниз,
в результате чего в корне оказывается второй по величине элемент.
Переставляем его в конец и повторяем операцию. Так потихоньку массив
отсортируется.

На каждом шаге мы \\(n \\) элементов проталкиваем на глубину не большую,
чем \\(\log n \\). Так мы получаем гарантированную оценку сложности
\\(O(n\log n) \\), однако проблема в том, что эта штука всегда работает
за \\(O(n\log n) \\), даже если ей дать уже отсортированный массив.
Из-за этого она проигрывает по скорости многим другим сортировкам.

"""
def heapify(a, i, max_depth):
    left = 2 * i + 1
    right = 2 * i + 2
    maximum = i
    if right < max_depth and a[right] > a[i]:
        maximum = right
    if left < max_depth and a[left] > a[maximum]:
        maximum = left
    if maximum != i:
        tmp = a[i]
        a[i] = a[maximum]
        a[maximum] = tmp
        heapify(a, maximum, max_depth)

def heap_sort(a):
    # Новая реализация heapsort
    # Алексей Башлыков

    for i in range(len(a) // 2, -1, -1):
        heapify(a, i, len(a))

    size = len(a)
    for i in range(len(a) - 1, -1, -1):
        a[0], a[i] = a[i], a[0]
        size -= 1
        heapify(a, 0, size)
    return a

def old_slow_heap_sort(a):
    #  Старая реализация — медленна и убога...

    def l_ch(i):
        # Left child
        return i * 2 + 1

    def r_ch(i):
        # Right child
        return i * 2 + 2

    def push_down(i, max_depth):
        # `max_depth` нужна, чтобы не трогать отсортированную часть кучи

        get_gt = lambda i, j: i if a[i] > a[j] else j

        while l_ch(i) < max_depth:
            # Выбираем элемент, на место которого нужно протолкнуть корень
            gt_ch = (get_gt(l_ch(i), r_ch(i))
                     if r_ch(i) < max_depth else
                     l_ch(i))

            if a[i] < a[gt_ch]:
                a[i], a[gt_ch] = a[gt_ch], a[i]
            else:
                break

            i = gt_ch

    # Строим кучу
    for i in range((len(a) // 2) - 1, -1, -1):
        push_down(i, len(a))

    # Сортируем кучу
    for i in range(len(a) - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        push_down(0, i)

    return a

#d

"""
## Тестирование сортировок

[[tests.py]]

__Тест на случайно упорядоченных массивах (T[n]):__

![Test 1](../images/sorts_t1.png)
![Test 2](../images/sorts_t2.png)
![Test 3](../images/sorts_t3.png)

"""
if __name__ == '__main__':
    functions = [
        # Название, тестируемая ф-я, ограничитель
        ['Selection sort', selection_sort, lambda n: n > 100],
        ['Insertion sort', insertion_sort, lambda n: n > 10000],
        ['Merge sort', merge_sort, None],
        ['Qsort in place', quick_sort_inplace, None],
        ['Quick sort', quick_sort, None],
        ['Heap sort', heap_sort, None],
        ['Old heap sort', old_slow_heap_sort, lambda n: n > 100000],
    ]

    for n, f, c in functions:
        a = list(range(100)) + list(range(50))
        random.shuffle(a)
        result = f(a)
        expected = sorted(list(range(100)) + list(range(50)))
        try:
            assert result == expected
        except AssertionError:
            print('Output:', result)
            print('Expected:', expected)
            raise AssertionError('ERROR! ' + n + ' is incorrect!')

    # Тест на случайно упорядоченных массивах
    def test_preparer(n):
        array = list(range(n))
        random.shuffle(array)
        return [array]

    tests.timetest(functions,
                   range_set=([(n, test_preparer)
                               for n in range(0, 501, 1)],
                              [(n, test_preparer)
                               for n in range(0, 10100, 100)],
                              [(n, test_preparer)
                               for n in range(0, 105000, 5000)],
                              ),
                   time_to_repeat=10,
                   output='csv')
