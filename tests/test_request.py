from unittest import mock

import pytest

import env
from api.request import *


def parse_to_list(string):
    return list(map(int, string.split(',')))


def test_errors():
    key = 'request_param_key'
    message = 'an error message'
    diff_key = 'different_request_param_kay'
    errors = Errors()
    assert errors.empty()
    errors.add(key, message)
    assert errors.present()
    assert errors.errors == {key: message}
    errors.add(diff_key, message)
    assert errors.errors == {key: message, diff_key: message}

def test_request_parser():
    args = {
        'integer': '123',
        'notint': '12a',
        'toobigint': '12345',
        'nottoobigint': '1234',
        'justenough': '12,13,14',
        'toofew': '12,13',
        'toomany': '12,13,14,15',
    }
    required_args = {
        'integer': int,
        'notint': int,
        'toobigint': int,
        'nottoobigint': int,
        'notincluded': int,
        'justenough': parse_to_list,
        'toofew': parse_to_list,
        'toomany': parse_to_list,
    }
    restrictions = {
        'toobigint': {'upper_bound': 10000},
        'nottoobigint': {'upper_bound': 10000},
        'justenough': {'count': 3},
        'toofew': {'count': 3},
        'toomany': {'count': 3},
    }
    expected_errors = {
        'notint': 'key was provided but could not be parsed',
        'toobigint': 'invalid: must be less than 10000',
        'notincluded': 'key is required, but was missing',
        'toofew': 'invalid: must include exactly 3 elements',
        'toomany': 'invalid: must include exactly 3 elements',
    }
    expected_parsed_args = {
        'integer': 123,
        'nottoobigint': 1234,
        'justenough': [12, 13, 14],
    }
    parser = RequestParser(args, required_args, restrictions)
    assert parser.errors.empty()
    assert parser.parsed_args == dict()

    parser.parse()
    assert parser.errors.errors == expected_errors
    assert parser.parsed_args == expected_parsed_args

def test_request_with_parse_error():
    args = {'integer': '123a'}
    function = abs
    required_args = {'integer': int}
    expected_errors = {'integer': 'key was provided but could not be parsed'}
    req = Request(args, function, required_args)
    assert req.process() == {'err': expected_errors, 'ok': None}

def test_request_with_missing_key_error():
    args = {'wrong_key': '123'}
    function = abs
    required_args = {'integer': int}
    expected_errors = {'integer': 'key is required, but was missing'}
    req = Request(args, function, required_args)
    assert req.process() == {'err': expected_errors, 'ok': None}

def test_request_with_upper_bound_error():
    args = {'integer': '12345'}
    function = abs
    required_args = {'integer': int}
    restrictions = {'integer': {'upper_bound': 100}}
    expected_errors = {'integer': 'invalid: must be less than 100'}
    req = Request(args, function, required_args, restrictions)
    assert req.process() == {'err': expected_errors, 'ok': None}

def test_request_with_count_error():
    args = {'numbers': '1,2,3,4,5'}
    function = sum
    required_args = {'numbers': parse_to_list}
    restrictions = {'numbers': {'count': 3}}
    expected_errors = {'numbers': 'invalid: must include exactly 3 elements'}
    req = Request(args, function, required_args, restrictions)
    assert req.process() == {'err': expected_errors, 'ok': None}

def test_request_with_operation_error():
    import math
    args = {'integer': '-123'}
    function = math.sqrt
    required_args = {'integer': int}
    expected_errors = {'operation': 'unknown error occurred'}
    req = Request(args, function, required_args)
    assert req.process() == {'err': expected_errors, 'ok': None}

def test_successful_request_with_one_arg():
    args = {'integer': '-123'}
    function = abs
    required_args = {'integer': int}
    req = Request(args, function, required_args)
    assert req.process() == {'err': {}, 'ok': 123}

def test_successful_request_with_one_comma_separated_arg():
    args = {'numbers': '1,2,3,4,5'}
    function = sum
    required_args = {'numbers': parse_to_list}
    restrictions = {'numbers': {'count': 5}}
    req = Request(args, function, required_args, restrictions)
    assert req.process() == {'err': {}, 'ok': 1+2+3+4+5}

def test_successful_request_with_multiple_args():
    args = {'a': '5', 'b': '6'}
    function = lambda x: x['a'] * x['b']
    required_args = {'a': int, 'b': int}
    req = Request(args, function, required_args)
    assert req.process() == {'err': {}, 'ok': 30}

