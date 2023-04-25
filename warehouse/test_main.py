import pytest
from warehouse import main


def test_create():
    pass


# def test_get_nd_without_arguments():
#    with pytest.raises(TypeError):
#        main.get_normal_distribution()


# def test_get_nd_for_null():
#    assert main.get_normal_distribution(0, 0) == 0


def test_square_deviation_args():
    assert main.square_deviation(0, 0) == 0


def test_sd_div_variance():
    assert main.square_deviation(0, 0) / main.variance(1) == 0


def test_exp_from_sd_div_v():
    assert main.exp(main.square_deviation(0, 0) / main.variance(1)) == 1


def test_variance():
    assert main.variance(2) == 8


def test_integr_sum():
    assert main.integr_sum(10) == 25.06628274631


def test_nd():
    assert main.get_normal_distribution(0, 0, 1) == 0.3989422804014327


def test_equal_nd():
    assert main.get_normal_distribution(0, 0, 1) == main.normal(0, 0, 1)
