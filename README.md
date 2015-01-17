# Конспекты лекций по предмету «алгоритмы и структуры данных»

 __Ведущий:__ Объедков Сергей Александрович

 Конспектировал Гончаров Владимир

ВШЭ, ФКН, ПМИ, 2015 (1 курс II поток)


## Содержание

*   [1: Оценка сложности алгоритмов, сортировки][l1]
    *   [Оценка сложности алгоритмов][l1.1]
    *   [Сортировка выбором (selection sort)][l1.2]
    *   [Сортировка вставками (insertion sort)][l1.3]
    *   [Сортировка слиянием (merge sort)][l1.4]
    *   [Быстрая сортировка (qsort)][l1.5]


## Сборка

Эти лекции доступны для правки всем желающим. Если вы хотите что-то добавить,
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


[l1]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html
[l1.1]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-2
[l1.2]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-4
[l1.3]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-6
[l1.4]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-8
[l1.5]: http://amatanhead.github.io/Programming-lectures/lectures/sorts.html#section-10
