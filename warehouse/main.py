"""
Создание числового нормального распределения по N обьектам
"""
import math
from math import exp, pi


def get_nd(n: int) -> list[float]:
    if n % 2 == 0:
        middle = (n + 1) / 2.0
    else:
        middle = n // 2 + 1
    print(f"\n{middle}")
    sigma = 1
    lst = []
    for i in range(1, n + 1):
        # print(i)
        sd = square_deviation(i, middle)
        sd_div_s = sd_div_sigma(sd, sigma)
        exp_sd = exp(sd_div_s)
        ndi = normal_distribution(exp_sd, sigma)
        lst.append(ndi)

    return lst


def square_deviation(x: float | int, m: float) -> float:
    return -pow(x - m, 2)


def sd_div_sigma(x: float, s: float) -> float:
    return x / (2 * s * s)


def normal_distribution(x: float, s: float) -> float:
    return round(x / (pow(2 * pi, 1 / 2) * s) * 100, 2)
