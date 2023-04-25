"""
Создание числового нормального распределения по N обьектам
"""
import math
from math import exp
from numpy.random import normal


def square_deviation(x: float, m: float):
    return pow(x - m, 2)


def variance(s: float):
    return 2 * s * s


def integr_sum(s: float):
    return pow(2 * math.pi, 1 / 2) * s


def get_normal_distribution(x: float, m: float, s: float) -> float:
    return exp(-square_deviation(x, m) / variance(s)) / integr_sum(s)


def sigma(x):
    # x = [0, 100]
    mean = sum(x) / len(x)
    sig = pow(sum([pow(y - mean, 2) for y in x]) / len(x), 1 / 2)
    return sig


if __name__ == '__main__':
    # print(get_normal_distribution(0, 0, 1))
    """for i in range(50):
        for _ in range(100):
            ss = list(map(int, normal(50, i, 5)))
            for t in ss:
                if t > 100 or t < 0:
                    print('*' * 40)
                    print(i)
                    print(ss)
                    print(sigma(ss))"""
    ss = list(map(lambda x: x, normal(0, 10, 5)))
    print(ss)
    print(sigma(ss))
