import pytest
from warehouse import normal_distribution


# def test_get_nd_without_arguments():
#    with pytest.raises(TypeError):
#        main.get_normal_distribution()

def test_create():
    normal_distribution.get_nd(5)


def test_square_deviation():
    assert normal_distribution._square_deviation(x=1, m=3) == -4


def test_sd_div_sigma():
    assert normal_distribution._sd_div_sigma(x=-4, s=1) == -2


def test_exp():
    assert normal_distribution.exp(-2) == 0.1353352832366127


def test_normal_distribution():
    assert normal_distribution._normal_distribution(x=0.1353352832366127, s=1) == 5.40


def test_get_nd_for_five():
    assert normal_distribution.get_nd(5) == [5.4, 24.2, 39.89, 24.2, 5.4]


def test_get_nd_for_six():
    assert normal_distribution.get_nd(6) == [1.75, 12.95, 35.21, 35.21, 12.95, 1.75]


def test_get_nd_for_three():
    assert normal_distribution.get_nd(3) == [24.2, 39.89, 24.2]


def test_get_weigth_for_nd():
    assert normal_distribution.get_weigth_for_nd(target=100, nd=[1.75, 12.95, 35.21, 35.21, 12.95, 1.75]) == 2.84


def test_sum_of_nd():
    #assert 99 < sum(main.get_nd(1)) <= 100
    #assert 99 < sum(main.get_nd(2)) <= 100
    #assert 99 < sum(main.get_nd(3)) <= 100
    #assert 99 < sum(main.get_nd(4)) <= 100
    assert 99 < sum(normal_distribution.get_nd(5)) <= 100
    assert 99 < sum(normal_distribution.get_nd(6)) <= 100
