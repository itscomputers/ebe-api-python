from random import randint

from api import db, ebe
from api.models import Factorization

def gcd(numbers):
    return ebe.gcd(*numbers)

def lcm(numbers):
    return ebe.lcm(*numbers)

def bezout(numbers):
    return ebe.bezout(*numbers)

def is_prime(number, display=False):
    primality = ebe.is_prime(number)
    if display:
        return 'yes' if primality else 'no'
    return primality

def next_prime(number):
    return ebe.next_prime(number)

def random_prime(digits):
    lower = 10**(digits - 1)
    return next_prime(randint(lower, 10*lower))

<<<<<<< HEAD
def factorization(number):
    return Factorization.find_or_create(str(number)).factor_list()

def two_squares(number):
    return Factorization.find_or_create(str(number)).two_squares()

def four_squares(number):
    return Factorization.find_or_create(str(number)).four_squares()

