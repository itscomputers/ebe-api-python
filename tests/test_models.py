import pytest
from functools import reduce

import env
from api import db
from api.models import *

def test_compute_prime():
    prime = Prime(number=4567)

    assert prime.prime is None
    assert prime.invalid()
    prime.compute()
    assert prime.prime is True
    assert not prime.invalid()

def product(factor_list):
    return reduce(lambda x, y: x * y, factor_list, 1)

def test_compute_factorization():
    factor_list = [2, 3, 3, 541]
    factorization = Factorization(number=product(factor_list))

    assert factorization.factors is None
    assert factorization.invalid()
    factorization.compute()
    assert factorization.factors == ','.join(map(str, factor_list))
    assert not factorization.invalid()

def test_factor_list():
    factor_list = [2, 3, 3, 541]
    factorization = Factorization(number=product(factor_list)).compute()
    assert not hasattr(factorization, '_factor_list')
    assert factorization.factor_list() == factor_list
    assert factorization._factor_list == factor_list

def test_factorization():
    factor_list = [2, 3, 3, 541]
    factorization = Factorization(number=product(factor_list)).compute()
    assert not hasattr(factorization, '_factorization')
    assert factorization.factorization() == {2: 1, 3: 2, 541: 1}
    assert factorization._factorization == {2: 1, 3: 2, 541: 1}

def test_two_squares():
    factor_list = [2, 3, 3, 541]
    two_squares = Factorization(number=product(factor_list)).compute().two_squares()
    assert sum(map(lambda x: x**2, two_squares)) == product(factor_list)

    factor_list = [2, 3, 541]
    two_squares = Factorization(number=product(factor_list)).compute().two_squares()
    assert two_squares is None

def test_four_squares():
    factor_list = [2, 3, 3, 541]
    four_squares = Factorization(number=product(factor_list)).compute().four_squares()
    assert sum(map(lambda x: x**2, four_squares)) == product(factor_list)

    factor_list = [2, 3, 541]
    four_squares = Factorization(number=product(factor_list)).compute().four_squares()
    assert sum(map(lambda x: x**2, four_squares)) == product(factor_list)


