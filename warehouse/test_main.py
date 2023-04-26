import pytest
from warehouse import main


# def test_get_nd_without_arguments():
#    with pytest.raises(TypeError):
#        main.get_normal_distribution()

def test_create():
    main.get_nd(5)


def test_square_deviation():
    assert main.square_deviation(x=1, m=3) == -4


def test_sd_div_sigma():
    assert main.sd_div_sigma(x=-4, s=1) == -2


def test_exp():
    assert main.exp(-2) == 0.1353352832366127


def test_normal_distribution():
    assert main.normal_distribution(x=0.1353352832366127, s=1) == 5.40


def test_get_nd_for_five():
    assert main.get_nd(5) == [5.4, 24.2, 39.89, 24.2, 5.4]


def test_get_nd_for_six():
    assert main.get_nd(6) == [1.75, 12.95, 35.21, 35.21, 12.95, 1.75]


def test_get_nd_for_three():
    assert main.get_nd(3) == [24.2, 39.89, 24.2]
