from collections import Counter
from api import db, ebe

#===========================================================

class ModelMixin:
    @classmethod
    def find(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def find_or_create(cls, number, attrs=None):
        model = cls.find(number)
        if model is None:
            model = cls(number=number)
            if attrs is not None:
                for key, value in attrs.items():
                    setattr(model, key, value)
            model.save()

        return model

    @classmethod
    def bulk_find_or_create(cls, numbers):
        models = []
        for number in numbers:
            model = cls.find(number)

            if model is None:
                model = cls(number=number)

            if model.invalid():
                model.compute()
                db.session.add(model)

            models.append(model)

        db.session.commit()
        return models

    def invalid(self):
        return NotImplemented

    def compute(self):
        return NotImplemented

    def save(self):
        if self.invalid():
            self.compute()

        db.session.add(self)
        db.session.commit()

        return self

#===========================================================

class Prime(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True)
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
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True)
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

