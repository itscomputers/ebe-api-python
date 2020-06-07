from random import randint
from flask import jsonify, request

from api import api, methods, utils
from api.request import Request

#-----------------------------

@api.route('/', methods=['GET'])
def home():
    return "<h1>ebe -- a number theory library in python</h1>"

#-----------------------------

@api.route('/api/v1/docs', methods=['GET'])
def docs():
    return None

#-----------------------------

@api.route('/api/v1/gcd', methods=['GET'])
def gcd():
    return jsonify(Request(
        request.args,
        methods.gcd,
        required_args={'numbers': utils.string_to_int_list},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/lcm', methods=['GET'])
def lcm():
    return jsonify(Request(
        request.args,
        methods.lcm,
        required_args={'numbers': utils.string_to_int_list},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/bezout', methods=['GET'])
def bezout():
    return jsonify(Request(
        request.args,
        methods.bezout,
        required_args={'numbers': utils.string_to_int_list},
        restrictions={'numbers': {'count': 2}},
    ).process(
        lambda x: list(map(str, x))
    ))

#-----------------------------

@api.route('/api/v1/is_prime', methods=['GET'])
def is_prime():
    return jsonify(Request(
        request.args,
        methods.is_prime,
        required_args={'number': int},
    ).process())

#-----------------------------

@api.route('/api/v1/next_prime', methods=['GET'])
def next_prime():
    return jsonify(Request(
        request.args,
        methods.next_prime,
        required_args={'number': int},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/random_prime', methods=['GET'])
def random_prime():
    return jsonify(Request(
        request.args,
        methods.random_prime,
        required_args={'digits': int},
        restrictions={'digits': {'upper_bound': 100}},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/factorization', methods=['GET'])
def factorization():
    return jsonify(Request(
        request.args,
        methods.factorization,
        required_args={'number': int},
        restrictions={'number': {'upper_bound': 10**30}},
    ).process())

#-----------------------------

@api.route('/api/v1/two_squares', methods=['GET'])
def two_squares():
    return jsonify(Request(
        request.args,
        methods.two_squares,
        required_args={'number': int},
        restrictions={'number': {'upper_bound': 10**30}},
    ).process())

#-----------------------------

@api.route('/api/v1/four_squares', methods=['GET'])
def four_squares():
    return jsonify(Request(
        request.args,
        methods.four_squares,
        required_args={'number': int},
        restrictions={'number': {'upper_bound': 10**30}},
    ).process())

