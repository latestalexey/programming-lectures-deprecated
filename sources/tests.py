# coding: utf-8

import random
import timeit
from operator import itemgetter


"""
## Тестирование скорости

Input:

*  `functions`: Tuple of functions to be tested.
    Format is `((name, _callable, max_n), ...)` where
    *   `name` is human-readable name to display,
    *   `_callable` is a function _callable,
    *   `max_n` is maximum input length. The _callable will not be tested
        on arrays of length bigger than `max_n`.
        Sets infinite if none.
*  `range_set`: array with iterables to run with each test.
    format is `((range, shuffler), ...)` where
    *   `range` is source array elements. For example range(n).
    *   `shuffler` is a callable which runs before each test.
        For example `lambda x: random.shuffle(list(x)) is None and x`
        which shuffles elements in `x` and then returns it.
*  `time_to_repeat`: Each test runs `time_to_repeat` times.
*  `output`: set `'csv'` so you can run is like `python test.py > results.csv`

"""
def timetest(functions,
             range_set=(),
             time_to_repeat=10,
             output=None):

    for _range in range_set:
        if output == 'csv':
            print('n;' + ';'.join(map(itemgetter(0), functions)))
            print('')

        for a, shuffler in _range:
            a = list(a)
            n = len(a)

            tests = []

            for function in functions:
                if len(function) < 3:
                    function += [None] * (3 - len(function))
                name, _callable, max_n = function

                if (max_n is None) or (n <= max_n):
                    shuffler(a)
                    t = timeit.Timer(lambda: _callable(a))
                    tests.append([name,
                                  t.timeit(number=time_to_repeat)
                                  / time_to_repeat])
                elif output == 'csv':
                    tests.append([name, None])

            if output == 'csv':
                print(str(n) + ';' + ';'.join(
                    map(lambda x: str(x[1] or '').replace('.', ','), tests)
                ))
            else:
                print('n = ' + str(n))
                print('=' * len('n = ' + str(n)))

                for name, time in sorted(tests, key=itemgetter(1)):
                    print(name + ':\t', '%.10f' % time, 'sec')

                print('\n')

        if output == 'csv':
            print('~' * 3)
        else:
            print('~' * 80, '\n')
