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
import tests
from cmath import exp, pi
from mp_helpers import BigInt

"""
## Алгоритм Карацубы

Банальное произведение чисел в столбик работает за время \\(O(n^2) \\),
где \\(n \\)&nbsp;— количество цифр. Алгоритм Карацубы&nbsp;— первый алгоритм,
улучшающий эту оценку.

Итак, пусть у нас есть два \\(n \\)-разрядных числа \\(a \\), \\(b \\),
записанных в некоторой системе счисления по основанию \\(B \\).

Представим числа \\(a = \overline{a_{n-1} a_{n-2} \dots a_{0}} \\),
\\(b = \overline{b_{n-1} b_{n-2} \dots b_{0}} \\).

Каждое из этих чисел можно «разделить» на два числа&nbsp;— половинки длинны
\\(m = \frac n2 \\):

\\(a = a_0 + B^m \cdot a_1; \\\\
   b = b_0 + B^m \cdot b_1; \\)

Сделать это легко, мы буквально делим их:

\\(a_0 = \overline{a_{m-1} a_{m-2} \dots a_{0}}; \\\\
   a_1 = \overline{a_{n-1} a_{n-2} \dots a_{m}}; \\\\
   b_0 = \overline{b_{m-1} b_{m-2} \dots b_{0}}; \\\\
   b_1 = \overline{b_{n-1} b_{n-2} \dots b_{m}}; \\)

При этом операция умножения на \\(B^m \\)&nbsp;— на самом деле побитовый сдвиг.

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
    # Медленный, но показывающий суть алгоритм
    # Слишком медленный...
    # С какой-то огромной кучей копирований...

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

#d

"""
## Быстрое преобразование Фурье (FFT)

(см.: [1](http://jeremykun.com/2012/07/18/the-fast-fourier-transform/),
[2](http://habrahabr.ru/post/113642/))

__Прямое преобразование:__

Пусть дан многочлен \\(n \\)-й степени
\\(P_n = a_0 + a_1x + a_2x^2 + \dots + a_{n - 1}x^{n - 1} \\).

Тогда \\(\FFT (P_n) =
    [P_n(\omega_n^0), P_n(\omega_n^1), P_n(\omega_n^2), \dots,
    P_n(\omega_n^{n - 1})] \\), где \\(\omega_n^{k} = e^{\frac{2\pi ik}{n}} \\)&nbsp;—
    \\(k \\)-й комплексный корень \\(n \\)-й степени из единицы.

Примечательно, что алгоритм работает за \\(O(n\log n) \\). Пусть

\\(A(x) = a_0 + xa_2 + x^2a_4 + \dots + x^{n/2-1}a_{n-2} \\),
\\(B(x) = a_1 + xa_3 + x^2a_5 + \dots + x^{n/2-1}a_{n-1} \\)

тогда \\(P_n = A(x^2) + xB(x^2) \\). Применяя принцип «разделяй и
властвуй» можно рекурсивно вычислить БПФ:
\\(P(\omega_i)=A(\omega_{2i})+\omega_iB(\omega_{2i}) \\).
Тогда получаем классическую оценку на время
\\(T[n] = 2T[n/2] + O(n) = O(n\log n) \\).

Кстати, чтобы задача разделилась на подзадачи хорошо, нужно,
чтобы степерь многочлена была степенью двойки, т. е. \\(n=2^k \\).

__Обратное преобразование (IFFT):__

Обратное преобразование выполняется за то же самое время тем же
самым алгоритмом. Для этого нужно ко входным данным применить
сопряжение, а к выходным&nbsp;— деление на степень многочлена.
Несложно видеть, что легко это доказать =)

"""
def cached(f):
    # Небольшой декоратор для кэширования результатов функций

    cache = {}

    def out_function(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    return out_function

@cached
def omega(n, k):
    return exp((2.0j * pi * k) / n)

def fft(x):
    n = len(x)
    if n == 1:
        return x
    else:
        even = fft(x[::2])
        odd = fft(x[1::2])

        combined = [0] * n
        for m in range(n // 2):
            combined[m] = even[m] + omega(n, -m) * odd[m]
            combined[m + n // 2] = even[m] - omega(n, -m) * odd[m]

        return combined

def ifft(x):
    return [j.real / len(x) for j in fft([i.conjugate() for i in x])]

#d

"""
## Умножение чисел через БПФ

Заметим, что \\(\FFT(A \cdot B) = [\FFT(A) \cdot \FFT(B)] \\),
где \\([\FFT(A) \cdot \FFT(B)] \\)&nbsp;— покоординатное призведение двух массивов.
Тогда \\(A \cdot B = \IFFT([\FFT(A) \cdot \FFT(B)]) \\). Легко убедиться, что
сложность алгоритма&nbsp;— \\(O(n\log n \log\log n) \\). \\(\log\log n \\)&nbsp;— время,
уходящее на работу с числами. Поскольку нормальзацию мы применяем лишь
в конце, числа в разрядах получаются большими.

"""
def pad(x):
    i = 0
    while 2 ** i < len(x):
        i += 1
    return x + [0] * (2 ** i - len(x))

def fft_multiply(a_source, b_source):
    a = pad(a_source.bytes)
    b = pad(b_source.bytes)
    if len(a) > len(b):
        b += [0] * (len(a) - len(b))
    elif len(b) > len(a):
        a += [0] * (len(b) - len(a))
    a += [0] * len(a)
    b += [0] * len(b)

    inv = ifft([i * j for i, j in zip(fft(a), fft(b))])

    for i in range(len(inv)):
        inv[i] = int(inv[i] + 0.5)
        if inv[i] > 9:
            inv[i + 1] += inv[i] // 10
            inv[i] %= 10

    res = BigInt()
    res.bytes = inv
    res.sign = a_source.sign * b_source.sign
    res.clean()

    return res
