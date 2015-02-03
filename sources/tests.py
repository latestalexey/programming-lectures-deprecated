# coding: utf-8

import random
import timeit
from operator import itemgetter


"""
## Тестирование скорости

Вход:

*  `functions`: Список функций для тестирования.
    Формат — `((name, _callable, denier), ...)`, где
    *   `name` читабельное имя, строка,
    *   `_callable` — тестируемая функция,
    *   `denier` — функция, получающая на вход аргументы,
        которые будут переданы в тест, и говорящая, можно ли проводить тест
        с этой функцией. Используется для того,
        чтобы в середине теста отключить алгоритмы, работающие слишком долго.
*  `range_set`: Массив из групп тестов.
    Каждая группа имеет формат: `((input, preparer), (input, preparer), ...)`,
    где
    *   `input` — данные, определяющие тест.
    *   `preparer` — функция, принимающая на вход `input` и возвращающая список
        аргументов, которые будут переданы в тестируемую функцию.
*   `time_to_repeat`: Каждый тест запускается `time_to_repeat` раз.
*   `output`: поставьте `'csv'` для вывода в формате `.csv`
    (`python test.py > results.csv`)

"""
def timetest(functions,
             range_set=(),
             time_to_repeat=10,
             output=None):

    for _range in range_set:
        if output == 'csv':
            print('n;' + ';'.join(map(itemgetter(0), functions)))
            print('')

        for input, preparer in _range:

            tests = []

            for name, _callable, denier in functions:
                if denier is None or not denier(input):
                    input_args = preparer(input)
                    t = timeit.Timer(lambda: _callable(*input_args))
                    tests.append([name,
                                  t.timeit(number=time_to_repeat)
                                  / time_to_repeat])
                elif output == 'csv':
                    tests.append([name, None])

            if output == 'csv':
                print(str(input) + ';' + ';'.join(
                    map(lambda x: str(x[1] or '').replace('.', ','), tests)
                ))
            else:
                print('input = ' + str(input))
                print('=' * len('n = ' + str(input)))

                for name, time in sorted(tests, key=itemgetter(1)):
                    print(name + ':\t', '%.10f' % time, 'sec')

                print('\n')

        if output == 'csv':
            print('~' * 3)
        else:
            print('~' * 80, '\n')
