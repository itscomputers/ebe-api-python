from collections import Counter
from api import db, ebe

#===========================================================

class ModelMixin:
    @classmethod
    def find(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def find_or_create(cls, number, attr=None, value=None):
        model = cls.find(number)
        if model is None:
            print("build model")
            model = cls(number=number)
            if attr is not None and value is not None:
                print("with {}={}".format(attr, value))
                setattr(model, attr, value)
            model.save()

        print("model: {}".format(model))
        return model

    def invalid(self):
        return NotImplemented

    def save(self):
        if self.invalid():
            self.compute()

        db.session.add(self)
        db.session.commit()

        return self

#===========================================================

class Prime(db.Model, ModelMixin):
    number = db.Column(db.Integer, primary_key=True)
    prime = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return "<Prime number={}, prime={}>".format(self.number, self.prime)

    def compute(self):
        self.prime = ebe.is_prime(self.number)
        return self

    def invalid(self):
        return self.prime is None

#===========================================================

class Factorization(db.Model, ModelMixin):
    number = db.Column(db.Integer, primary_key=True)
    factors = db.Column(db.String)

    def __repr__(self):
        return "<Factorization number={}, factors={}>".format(self.number, self.factors)

    def compute(self):
        factorization = ebe.factor(self.number)
        factors = sorted(Counter(factorization).elements())
        self.factors = ','.join(map(str, factors))
        return self

    def invalid(self):
        return self.factors is None

    def factor_list(self):
        if not hasattr(self, '_factor_list'):
            self._factor_list = list(map(int, self.factors.split(',')))
        return self._factor_list

    def factorization(self):
        if not hasattr(self, '_factorization'):
            self._factorization = dict(Counter(self.factor_list()))
        return self._factorization

    def two_squares(self):
        return ebe.two_squares(self.factorization())

    def four_squares(self):
        return ebe.four_squares(self.factorization())

