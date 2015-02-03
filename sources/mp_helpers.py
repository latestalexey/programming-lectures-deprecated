# coding: utf-8

import random
from copy import deepcopy


"""
## Класс для представления длинного числа

Абсолютно наивная и неэффективная реализация,
нужна лишь для того, чтобы хоть как-то проиллюстрировать
алгоритмы работы с длинной арифметикой.

"""

class BigInt(object):

    def clean(self):
        # Очистить ведущие нули

        while self.bytes[-1] == 0 and len(self.bytes) > 1:
            self.bytes.pop()

    def clone(self):
        result = BigInt()
        result.bytes = self.bytes
        result.sign = self.sign
        return result

    def __init__(self, init_number=0):

        self.bytes = []

        if init_number < 0:
            self.sign, init_number = -1, -init_number
        else:
            self.sign = 1

        while init_number:
            self.bytes.append(init_number % 10)
            init_number //= 10

        self.bytes.append(0)

        self.clean()

    # Доступ
    # ======

    def __len__(self):
        return len(self.bytes)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.bytes[key.start:key.stop:key.step]
        else:
            return self.bytes[key] if 0 <= key < len(self.bytes) else 0

    # Вывод
    # =====

    def __str__(self):
        if self.bytes == [0]:
            return '0'
        else:
            return (('-' * (self.sign == -1)) +
                    ''.join([str(self.bytes[i])
                             for i in range(len(self.bytes) - 1, -1, -1)]))

    # Сравнения
    # =========

    def __eq__(self, rvalue):
        return self.sign == rvalue.sign and self.bytes == rvalue.bytes

    def __neq__(self, rvalue):
        return not(self == rvalue)

    def __gt__(self, rvalue):
        if self.sign > rvalue.sign:
            return True

        i = max(len(self), len(rvalue))
        while (i >= 0) and self[i] == rvalue[i]:
            i -= 1
        return self[i] * self.sign > rvalue[i] * rvalue.sign

    def __lt__(self, rvalue):
        if self.sign < rvalue.sign:
            return True

        i = max(len(self), len(rvalue))
        while (i >= 0) and self[i] == rvalue[i]:
            i -= 1
        return self[i] * self.sign < rvalue[i] * rvalue.sign

    # Математика
    # ==========

    def __neg__(self):
        result = self.clone()
        result.sign = -self.sign
        return result

    def __iadd__(self, rvalue):
        # Сложение `a += b`

        if self.sign == -1 and rvalue.sign == 1:
            return rvalue - (-self)
        elif self.sign == 1 and rvalue.sign == -1:
            return self - (-rvalue)
        else:
            if len(self.bytes) < len(rvalue.bytes):
                self.bytes.extend([0 for _ in
                                   range(len(rvalue.bytes) - len(self.bytes))])
            self.bytes.append(0)

            for i in range(max(len(self.bytes), len(rvalue.bytes))):
                self.bytes[i] += rvalue[i]
                if self.bytes[i] > 9:
                    self.bytes[i + 1] += self.bytes[i] // 10
                    self.bytes[i] %= 10

            self.clean()
            return self

    def __add__(self, rvalue):
        # Сложение `a + b`
        result = self.clone()
        result += rvalue
        return result

    def __isub__(self, rvalue):
        # Вычитание `a -= b`

        if rvalue.sign == -1:
            return self + (-rvalue)
        elif self.sign == -1:
            return -(-self + rvalue)
        elif self < rvalue:
            return -(rvalue - self)
        else:
            if len(self.bytes) < len(rvalue.bytes):
                self.bytes.extend([0 for _ in
                                   range(len(rvalue.bytes) - len(self.bytes))])
            self.bytes.append(0)

            for i in range(max(len(self.bytes), len(rvalue.bytes))):
                if self[i] < rvalue[i]:
                    self.bytes[i] += 10
                    self.bytes[i + 1] -= 1
                self.bytes[i] -= rvalue[i]

            self.clean()
            return self

    def __sub__(self, rvalue):
        # Вычитание `a - b`
        result = self.clone()
        result -= rvalue
        return result

    def __imul__(self, rvalue):
        # Обычное умножение столбиком `a *= b`
        result = []
        result.extend([0 for _ in
                       range(len(rvalue.bytes) + len(self.bytes) + 1)])

        self.sign = self.sign * rvalue.sign

        for i in range(len(self.bytes)):
            for j in range(len(rvalue.bytes)):
                result[i + j] += self[i] * rvalue[j]

        self.bytes = result

        for i in range(len(self.bytes)):
            if self.bytes[i] > 9:
                self.bytes[i + 1] += self.bytes[i] // 10
                self.bytes[i] %= 10

        self.clean()
        return self

    def __mul__(self, rvalue):
        # Обычное умножение столбиком `a * b`
        result = self.clone()
        result *= rvalue
        return result

    def __ilshift__(self, rvalue):
        # Побитовый сдвиг влево `a <<= n`
        self.bytes = [0 for _ in range(rvalue)] + self.bytes
        return self

    def __lshift__(self, rvalue):
        # Побитовый сдвиг влево `a << n`
        result = self.clone()
        result <<= rvalue
        return result


if __name__ == '__main__':
    # Perform some tests on math operations
    for i in range(10000):
        a = random.randint(-1000, 1000)
        assert str(-BigInt(a)) == str(-a)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) > BigInt(b)) == str(a > b)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) < BigInt(b)) == str(a < b)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) == BigInt(b)) == str(a == b)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) != BigInt(b)) == str(a != b)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) + BigInt(b)) == str(a + b)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) - BigInt(b)) == str(a - b)

    for i in range(10000):
        a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
        assert str(BigInt(a) * BigInt(b)) == str(a * b)
