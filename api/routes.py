from random import randint
from flask import jsonify, redirect, render_template, request, url_for

from api import api, methods, utils
from api.request import Request

#-----------------------------

EBE_DICT = {
    'is_prime': { 
        'order': 100, 
        'method': 'is_prime', 
        'question': 'is it prime?',
        'answer': lambda x: methods.is_prime(x, display=True),
    },
    'next_prime': { 
        'order': 110, 
        'method': 'next_prime', 
        'question': 'what\'s the next prime?', 
        'answer': lambda x: methods.next_prime(x),
    },
    'factorization': {
        'order': 200,
        'method': 'factorization',
        'question': 'how does it factor?',
        'answer': lambda x: methods.factorization(x, display=True),
    },
    'two_squares': {
        'order': 210,
        'method': 'two_squares',
        'question': 'as a sum of two squares?',
        'answer': lambda x: methods.two_squares(x, display=True),
    },
    'four_squares': {
        'order': 210,
        'method': 'four_squares',
        'question': 'as a sum of four squares?',
        'answer': lambda x: methods.four_squares(x, display=True),
    },
}

EBE_LIST = sorted(EBE_DICT.values(), key=lambda x: x['order']) 

#-----------------------------

@api.route('/')
def home():
    return render_template('base.html', ebe_list=EBE_LIST)

#-----------------------------

def build_route(method, number=None):
    if request.method == 'POST':
        return redirect(url_for('{}_specific'.format(method), number=request.form['number']))
    method_details = EBE_DICT[method]
    question = method_details['question']
    answer = method_details['answer'](number) if number is not None else None
    return render_template(
        'question_answer.html', 
        number=number, 
        question=question, 
        answer=answer, 
        ebe_list=EBE_LIST
    )

#-----------------------------

@api.route('/is_prime/', methods=['GET', 'POST'])
@api.route('/is_prime', methods=['GET', 'POST'])
def is_prime():
    return build_route('is_prime')

@api.route('/is_prime/<int:number>', methods=['GET', 'POST'])
def is_prime_specific(number):
    return build_route('is_prime', number)

#-----------------------------

@api.route('/next_prime/', methods=['GET', 'POST'])
@api.route('/next_prime', methods=['GET', 'POST'])
def next_prime():
    return build_route('next_prime')

@api.route('/next_prime/<int:number>', methods=['GET', 'POST'])
def next_prime_specific(number):
    return build_route('next_prime', number)

#-----------------------------

@api.route('/factorization/', methods=['GET', 'POST'])
@api.route('/factorization', methods=['GET', 'POST'])
def factorization():
    return build_route('factorization')

@api.route('/factorization/<int:number>', methods=['GET', 'POST'])
def factorization_specific(number):
    return build_route('factorization', number)

#-----------------------------

@api.route('/two_squares/', methods=['GET', 'POST'])
@api.route('/two_squares', methods=['GET', 'POST'])
def two_squares():
    return build_route('two_squares')

@api.route('/two_squares/<int:number>', methods=['GET', 'POST'])
def two_squares_specific(number):
    return build_route('two_squares', number)

#-----------------------------

@api.route('/four_squares/', methods=['GET', 'POST'])
@api.route('/four_squares', methods=['GET', 'POST'])
def four_squares():
    return build_route('four_squares')

@api.route('/four_squares/<int:number>', methods=['GET', 'POST'])
def four_squares_specific(number):
    return build_route('four_squares', number)

#-----------------------------

@api.route('/api/v1/docs', methods=['GET'])
def docs():
    return None

#-----------------------------

@api.route('/api/v1/gcd', methods=['GET'])
def api_gcd():
    return jsonify(Request(
        request.args,
        methods.gcd,
        required_args={'numbers': utils.string_to_int_list},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/lcm', methods=['GET'])
def api_lcm():
    return jsonify(Request(
        request.args,
        methods.lcm,
        required_args={'numbers': utils.string_to_int_list},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/bezout', methods=['GET'])
def api_bezout():
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
def api_is_prime():
    return jsonify(Request(
        request.args,
        methods.is_prime,
        required_args={'number': int},
    ).process())

#-----------------------------

@api.route('/api/v1/next_prime', methods=['GET'])
def api_next_prime():
    return jsonify(Request(
        request.args,
        methods.next_prime,
        required_args={'number': int},
    ).process(
        str
    ))

#-----------------------------

@api.route('/api/v1/random_prime', methods=['GET'])
def api_random_prime():
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
def api_factorization():
    return jsonify(Request(
        request.args,
        methods.factorization,
        required_args={'number': int},
        restrictions={'number': {'upper_bound': 10**30}},
    ).process())

#-----------------------------

@api.route('/api/v1/two_squares', methods=['GET'])
def api_two_squares():
    return jsonify(Request(
        request.args,
        methods.two_squares,
        required_args={'number': int},
        restrictions={'number': {'upper_bound': 10**30}},
    ).process())

#-----------------------------

@api.route('/api/v1/four_squares', methods=['GET'])
def api_four_squares():
    return jsonify(Request(
        request.args,
        methods.four_squares,
        required_args={'number': int},
        restrictions={'number': {'upper_bound': 10**30}},
    ).process())

