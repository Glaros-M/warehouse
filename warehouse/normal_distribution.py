"""
Создание числового нормального распределения по N обьектам
Работа функции numpy.random.normal() не слишком подошла,
на основе формул в статье https://habr.com/ru/articles/730936/ разработал свою реализацию
"""
import math
from math import exp, pi


def _square_deviation(x: float | int, m: float) -> float:
    """Вычисляет квадратичное отклонение в точке x

    Аргументы:
    ----------
    x: float - Квадратичное отклонение _square_deviation()
    m: float - Мю, положение пика (середины) функции нормального распределения

    Возвращает:
    ----------
    float - промежуточное значение
    """
    return -pow(x - m, 2)


def _sd_div_sigma(x: float, s: float) -> float:
    """Вычисляет отношение квадратичного отклонения к 2*сигма
    Аргументы:
    ----------
    x: float - Квадратичное отклонение _square_deviation()
    s: float - Сигма, стандартное отклонение

    Возвращает:
    ----------
    float - промежуточное значение
    """
    return x / (2 * s * s)


def _normal_distribution(x: float, s: float) -> float:
    """Нормализует распределение таким образом что бы сумма непрерывных вероятностей равнялась 1

    Аргументы:
    ----------
    x: float - Экспонента отношения квадратичного отклонения с сигмой exp(_sd_div_sigma)
    s: float - Сигма, стандартное отклонение

    Возвращает:
    ----------
    float - величина вероятности в конкретной точке
    """
    return round(x / (pow(2 * pi, 1 / 2) * s) * 100, 2)


def get_nd(n: int, sigma: float = 1, to_int: bool = False) -> list[float]:
    """Генерация нормального распределения вероятностей длинной n

    Сигма установлена на 1.
    Центр распределения вычисляется относительно n. Таким образом что бы наибольшая вероятность приходилась
    на один или два центральных элемента списка.

    Аргументы:
    ----------
    n: int - длинна требуемого нормального распределения

    Возвращает:
    ----------
    lst: list[float] - нормальное распределение вероятностей из n элементов
    """

    if n % 2 == 0:
        middle = (n + 1) / 2.0
    else:
        middle = n // 2 + 1
    lst = []
    for i in range(1, n + 1):
        sd = _square_deviation(i, middle)
        sd_div_s = _sd_div_sigma(sd, sigma)
        exp_sd = exp(sd_div_s)
        ndi = _normal_distribution(exp_sd, sigma)
        lst.append(ndi)
    if to_int:
        return [int(x) for x in lst]

    return lst


def get_weigth_for_nd(target: int, nd: list[float]) -> float:
    if len(nd) % 2 == 0:
        n = len(nd) // 2
    else:
        n = len(nd) // 2 + 1

    return round(target / nd[n], 2)


if __name__ == '__main__':

    print(get_nd(5, 0.8, True))