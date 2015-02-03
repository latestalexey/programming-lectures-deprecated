# Конспекты лекций по предмету «алгоритмы и структуры данных»

__Лектор:__ Объедков Сергей Александрович

__Семинарист:__ Макаров Илья Андреевич

Конспектировал Гончаров Владимир

ВШЭ, ФКН, ПМИ, 2015 (1 курс II поток)


## Небольшая аннотация и отказ от ответственности

Материал, представленный здесь, является объединением
конспектов с лекций и семинаров.

В этих материалах встречаются ошибки и неточности, которые я стараюсь выправлять,
но полностью сделать это возможно не всегда, так что будьте внимательны
и всегда думайте своей головой.

Реализации алгоритмов, представленные здесь, призваны показать идею,
воспринимать их следует исключительно как псевдокод (это, в общем-то,
и есть псевдокод с лекций). Если вы нашли ошибку в алгоритме —
пожалуйста, сообщите мне.

Так же я провожу сравнение записанных тут алгоритмов по скорости работы.
Я не претендую на строгость проводимого анализа.
В целом результаты соответствуют теории:
то, что должно выполняться за O(n^2)&nbsp;— выполняется за O(n^2),
а то, что должно выполнятьзя за O(nlogn)&nbsp;— выполняется за O(nlogn).
Константы же могут розниться.


## Содержание

*   [1: Оценка сложности алгоритмов, время сортировок и основная теорема о рекуррентных соотношениях][l1]
    *    [Оценка сложности алгоритмов][l1.1]
    *    [Время сортировок][l1.2]
    *    [Разделяй и властвуй][l1.3]
    *    [Основная теорема о рекуррентных соотношениях (master theorem)][l1.4]
*   [2: Cортировки][l2]
    *   [Сортировка выбором (selection sort)][l2.1]
    *   [Сортировка вставками (insertion sort)][l2.2]
    *   [Сортировка слиянием (merge sort)][l2.3]
    *   [Быстрая сортировка (qsort)][l2.4]
    *   [Сортировка кучей (heap sort, пирамидальная сортировка)][l2.5]
    *   [Проверка времени выполнения][l2.6]
*   [3: Поиск медианы в произвольном массиве][l3]
    *    [`k`-ая порядковая статистика][l3.1]
    *    [Медиана медиан (Median of Medians, BFPRT)][l3.2]
*   [4: Произведение чисел][l4]
     *   [Алгоритм Карацубы][l4.1]
*   Утилиты
    *   [Тесты][utilities.tests]
    *   [Простая длинная арифметика][utilities.mp_helpers]


## Сборка

Эти конспекты доступны для правки всем желающим. Если вы хотите что-то добавить,
исправить или улучшить — не стесняйтесь, git PR к вашим услугам :)

На данный момент я планирую писать лекции в питоне: примеры кода и
теория в комментариях к нему. Файлы python автоматически конвертируются
в html страницы с помощью генератора документации.

Обратите внимание, что основная ветка в этом проекте — `gh-pages`, а не `master`.

### Компиляция html

Вам понадобится [форк `pycco`, поддерживающий MathJax](https://github.com/AmatanHead/pycco):

    $ pip install git+https://github.com/AmatanHead/pycco.git

Непосредственно компиляция файлов:

    $ pycco sources/*.py -d lectures/


[l1]: http://amatanhead.github.io/Programming-lectures/lectures/sorts_theory.html
[l1.1]: http://amatanhead.github.io/Programming-lectures/lectures/sorts_theory.html#section-3
[l1.2]: http://amatanhead.github.io/Programming-lectures/lectures/sorts_theory.html#section-5
[l1.3]: http://amatanhead.github.io/Programming-lectures/lectures/sorts_theory.html#section-7
[l1.4]: http://amatanhead.github.io/Programming-lectures/lectures/sorts_theory.html#section-9

[l2]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html
[l2.1]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-2
[l2.2]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-4
[l2.3]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-6
[l2.4]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-8
[l2.5]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-10
[l2.6]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-12

[l3]: http://amatanhead.github.io/Programming-lectures/lectures/median.html
[l3.1]: http://amatanhead.github.io/Programming-lectures/lectures/median.html#section-2
[l3.2]: http://amatanhead.github.io/Programming-lectures/lectures/median.html#section-4

[l4]: http://amatanhead.github.io/Programming-lectures/lectures/product.html
[l4.1]: http://amatanhead.github.io/Programming-lectures/lectures/product.html#section-2

[utilities.tests]: http://amatanhead.github.io/Programming-lectures/lectures/tests.html
[utilities.mp_helpers]: http://amatanhead.github.io/Programming-lectures/lectures/mp_helpers.html
