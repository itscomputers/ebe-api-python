class Errors:
    def __init__(self):
        self.errors = {}

    def add(self, key, message):
        self.errors[key] = message

    def empty(self):
        return self.errors == {}

    def present(self):
        return self.errors != {}

    def include(self, key):
        return key in self.errors

    def exclude(self, key):
        return key not in self.errors

#-----------------------------

class RequestParser:
    def __init__(self, args, required_args, restrictions={}):
        self.args = args
        self.required_args = required_args
        self.restrictions = restrictions

        self.parsed_args = dict()
        self.errors = Errors()


    def parse(self):
        for key, parse_function in self.required_args.items():
            self.parse_single(key, parse_function, self.restrictions.get(key))
        return self


    def parse_single(self, key, parse_function, restriction):
        if key in self.args:
            try:
                value = parse_function(self.args[key])
                self.handle_upper_bound_restriction(key, value, restriction)
                self.handle_count_restriction(key, value, restriction)

                if self.errors.exclude(key):
                    self.parsed_args[key] = value

            except TypeError:
                self.errors.add(key, "key was provided but could not be parsed")

        else:
            self.errors.add(key, "key is required, but was missing")


    def handle_upper_bound_restriction(self, key, value, restriction):
        upper_bound = restriction.get('upper_bound') if restriction else None
        if upper_bound is not None  and value > upper_bound:
            self.errors.add(key, "invalid: must be less than {}".format(upper_bound))


    def handle_count_restriction(self, key, value, restriction):
        count = restriction.get('count') if restriction else None
        if count is not None and len(value) != count:
            self.errors.add(key, "invalid: must include exactly {} elements".format(count))

#-----------------------------

class Request:
    def __init__(self, args, function, required_args, restrictions={}):
        self.args = args
        self.function = function

        parser = RequestParser(args, required_args, restrictions).parse()
        self.errors = parser.errors
        self.parsed_args = parser.parsed_args

        self.result = None


    def process(self, return_type='default'):
        if self.errors.present():
            return self.render(return_type)

        self.apply()
        return self.render(return_type)


    def apply(self):
        if len(self.parsed_args.values()) == 1:
            self.result = self.function(list(self.parsed_args.values())[0])
        else:
            self.result = self.function(self.parsed_args)


    def render(self, return_type='default'):
        if self.errors.present():
            result = None
        elif return_type == 'default':
            result = self.result
        else:
            result = return_type(self.result)

        return {'err': self.errors.errors, 'ok': result}

