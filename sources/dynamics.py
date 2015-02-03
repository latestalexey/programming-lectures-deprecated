# coding: utf-8

"""
__Динамическое программирование__

Материалы: лекция 30.01, 03.02

Лектор: Объедков Сергей Александрович<br>
Семинарист: Макаров Илья Андреевич<br>
Конспектировал Гончаров Владимир

"""

import random
import tests
from operator import itemgetter

"""
## Задача поиска двух ближайших точек

На вход подается массив координат точек. Найти две ближайшие.

Случай, когда точки заданы одной координатой прост:
сортируем и проходимся по всем точкам, рассматривая соседей.
На все про все \\(O(n\log n) \\).

Случай на плоскости уже интереснее.
Для его решения поступим следующим образом.

Первым делом отсортируем наш массив по координате \\(x \\) и \\(y \\)
(На выходе получим два отсортированных массива;
Время — \\(O(n\log n) \\)). Теперь мы запустим рекурсивную функцию,
которая-то и вернет нам две ближайшие точки.

В рекурсивной функции мы разделим массив точек на две части
относительно медианы (за \\(O(n) \\)) и рекурсивно найдем в каждой из частей
две ближайшие точки. Назовем кратчайшее расстояние,
известное на данный момент, \\(\delta \\).

![Points 1](../images/dynamics_i1.png)

Осталось проверить, нету ли таких точек, которые лежат в разных половинах,
и расстояние между ними короче, чем \\(\delta \\).
Для этого рассмотрим любую точку и заметим вот что:
если есть точка, расстояние до которой меньше, чем \\(\delta \\),
она непременно должна лежать в прямоугольнике со сторонами
\\(\delta \\) на \\(2\delta \\):

![Points 2](../images/dynamics_i2.png)

Но в таком прямоугольнике может уместиться не более шести точек, иначе
расстояние между ними станет меньше \\(\delta \\) и возникнет противоречие.

Тогда достаточно для каждой точки рассмотреть 6 следующих ее соседей
в отсортированном по \\(y \\) массиве.

Несложно убедиться, что время работы алгоритма
\\(T_{rec}[n] = 2T_{rec}[n / 2] + O(n) = O(n\log n) \\),
\\(T[n] = O(n\log n) + T_{rec}[n] = O(n\log n) \\)

__Сравнение с обычным алгоритмом (T[n]):__

![Test 1](../images/dynamics_t1.png)

"""

def distance_2(a, b):
    # Квадрат расстояния между точками
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def closest_pair_bruteforce(points):
    # Алгоритм, работающий за O(n^2).
    # Нужен для выхода из рекурсии и для проверки

    assert len(points) >= 2

    min_dist = distance_2(points[0], points[1])
    min_points = (points[0], points[1])
    for point1 in points:
        for point2 in points:
            if point1 != point2 and distance_2(point1, point2) < min_dist:
                min_dist = distance_2(point1, point2)
                min_points = (point1, point2)
    return min_points

def closest_pair(points):
    # points = [(x1, y1), (x2, y2), ...]

    assert len(points) >= 2

    points_x = sorted(points, key=itemgetter(0))
    points_y = sorted(points_x, key=itemgetter(1))

    def closest_pair_recursive(points_x, points_y):
        if len(points_x) <= 3:
            return closest_pair_bruteforce(points_x)
        else:
            mid = len(points_x) // 2
            points_x_l, points_x_r = points_x[:mid], points_x[mid:]
            points_y_l, points_y_r = [], []
            for point in points_y:
                if point[0] <= points_x_l[-1][0]:
                    points_y_l.append(point)
                else:
                    points_y_r.append(point)

            l0, l1 = closest_pair_recursive(points_x_l, points_y_l)
            r0, r1 = closest_pair_recursive(points_x_r, points_y_r)
            d1, d2 = distance_2(l0, l1), distance_2(r0, r1)

            if d1 < d2:
                min_dist = d1
                min_points = l0, l1
            else:
                min_dist = d2
                min_points = r0, r1

            for i in range(len(points_y) - 1):
                for j in range(i + 1, min(i + 7, len(points_y))):
                    if distance_2(points_y[i], points_y[j]) < min_dist:
                        min_dist = distance_2(points_y[i], points_y[j])
                        min_points = points_y[i], points_y[j]

            return min_points

    return closest_pair_recursive(points_x, points_y)


if __name__ == '__main__':
    def generate_points(n):
        points = []
        for j in range(n):
            x, y = random.randint(-100 * n, 100 * n), random.randint(-100 * n, 100 * n)
            while (x, y) in points:
                x = random.randint(-100 * n, 100 * n)
                y = random.randint(-100 * n, 100 * n)
            points.append((x, y))
        return points

    for i in range(100):
        points = generate_points(100)

        p1 = closest_pair(points)
        p2 = closest_pair_bruteforce(points)

        try:
            assert distance_2(*p1) == distance_2(*p2)
        except AssertionError:
            print('Output:', distance_2(*p1), p1)
            print('Expected:', distance_2(*p2), p2)
            print('Input:', points)
            print('ERROR! Closest pair is incorrect!')

    functions = [
        ['Closest pair', closest_pair, None],
        ['Bruteforce', closest_pair_bruteforce, lambda n: n > 250],
    ]

    test_preparer = lambda n: [generate_points(n)]
    tests.timetest(functions,
                   range_set=([(n, test_preparer)
                               for n in range(2, 501, 1)],
                              ),
                   time_to_repeat=10,
                   output='csv')
