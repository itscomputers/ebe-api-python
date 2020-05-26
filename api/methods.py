from random import randint

from api import db, ebe
from api.models import Prime, Factorization

def gcd(numbers):
    return ebe.gcd(*numbers)

def lcm(numbers):
    return ebe.lcm(*numbers)

def bezout(numbers):
    return ebe.bezout(*numbers)

def is_prime(number):
    return Prime.find_or_create(number).prime

def next_prime(number):
    prime = ebe.next_prime(number)
    Prime.find_or_create(number=prime, attrs={'prime': True})
    return prime

def random_prime(digits):
    lower = 10**(digits - 1)
    prime = ebe.next_prime(randint(lower, 10*lower))
    Prime.find_or_create(number=prime, attrs={'prime': True})
    return prime

def factorization(number):
    return Factorization.find_or_create(number).factor_list()

def two_squares(number):
    return Factorization.find_or_create(number).two_squares()

def four_squares(number):
    return Factorization.find_or_create(number).four_squares()

