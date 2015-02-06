# coding: utf-8

"""
__Произведение чисел__

Материалы: лекция 27.01, семинар 02.02

Лектор: Объедков Сергей Александрович<br>
Семинарист: Макаров Илья Андреевич<br>
Конспектировал Гончаров Владимир

Для тестирования кода необходим класс для длинной арифметики:
[[mp_helpers.py]]

"""

import random
from mp_helpers import BigInt

"""
## Алгоритм Карацубы

Банальное произведение чисел в столбик работает за время \\(O(n^2) \\),
где \\(n \\) — количество цифр. Алгоритм Карацубы — первый алгоритм,
улучшающий эту оценку.

Итак, пусть у нас есть два \\(n \\)-разрядных числа \\(a \\), \\(b \\),
записанных в некоторой системе счисления по основанию \\(B \\).

Представим числа \\(a = \overline{a_{n-1} a_{n-2} \dots a_{0}} \\),
\\(b = \overline{b_{n-1} b_{n-2} \dots b_{0}} \\).

Каждое из этих чисел можно «разделить» на два числа — половинки длинны
\\(m = \frac n2 \\):

\\(a = a_0 + B^m \cdot a_1; \\\\
   b = b_0 + B^m \cdot b_1; \\)

Сделать это легко, мы буквально делим их:

\\(a_0 = \overline{a_{m-1} a_{m-2} \dots a_{0}}; \\\\
   a_1 = \overline{a_{n-1} a_{n-2} \dots a_{m}}; \\\\
   b_0 = \overline{b_{m-1} b_{m-2} \dots b_{0}}; \\\\
   b_1 = \overline{b_{n-1} b_{n-2} \dots b_{m}}; \\)

При этом операция умножения на \\(B^m \\) — на самом деле побитовый сдвиг.

Тогда:

\\(a \cdot b =
  ( a_0 + a_1 \cdot b^m ) \cdot ( b_0 + b_1 \cdot b^m ) = \\\\
  a_0 \cdot b_0 + a_0 \cdot b_1 \cdot b^m +
  a_1 \cdot b_0 \cdot b^m + a_1 \cdot b_1 \cdot b^{2m} = \\\\
  a_0 \cdot b_0 + ( a_0 \cdot b_1 + a_1 \cdot b_0 ) \cdot b^m +
  a_1 \cdot b_1 \cdot b^{2m} \\)

Заметим теперь, что \\( a_0 \cdot b_1 + a_1 \cdot b_0 =
( a_0 + a_1 ) \cdot ( b_0 + b_1 ) - a_0 \cdot b_0 - a_1 \cdot b_1 \\).
Тогда финальная формула:

\\(a \cdot b = \\\\
   a_0 \cdot b_0 + (( a_0 + a_1 ) \cdot ( b_0 + b_1 ) -
   a_0 \cdot b_0 - a_1 \cdot b_1 ) \cdot B^m + a_1 \cdot b_1 \cdot B^{2m} \\)

Заметим теперь, что в итоговой формуле мы имеем три умножения чисел
с \\(\frac n2 \\) разрядами, а все остальные операции выполняются
за \\(\Theta(n) \\). Тогда по основной теореме о рекуррентных соотношениях
получим оценку времени работы

\\(T[n] = 3T[n / 2] + \Theta(n) = O(n^{log_23}) \\)

"""
def karatsuba_algorithm(a, b):
    if len(a) <= 2 or len(b) <= 2:
        return a * b
    else:
        # Сий алгоритм безжалостно вмешивается во внутреннюю структуру
        # класса `BigInt`. Строго говоря, такое позволено лишь
        # членам класса, но мы не можем запихнуть эту функцию
        # внуть `BigInt`, ибо ее место здесь.

        sign = a.sign * b.sign

        if len(a) > len(b):
            b.bytes.extend([0 for _ in range(len(a) - len(b))])
        elif len(b) > len(a):
            a.bytes.extend([0 for _ in range(len(b) - len(a))])

        m = len(a) // 2

        a0 = BigInt()
        a0.bytes = a[0:m]
        a1 = BigInt()
        a1.bytes = a[m:len(a)]

        b0 = BigInt()
        b0.bytes = b[0:m]
        b1 = BigInt()
        b1.bytes = b[m:len(a)]

        a.clean()
        b.clean()

        a0b0 = karatsuba_algorithm(a0, b0)
        a1b1 = karatsuba_algorithm(a1, b1)

        result = (a0b0 +
                 ((karatsuba_algorithm((a0 + a1), (b0 + b1))
                  - a0b0 - a1b1) << m) +
                 (a1b1 << (2 * m)))
        result.sign = sign
        return result
