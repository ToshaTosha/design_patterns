from src.models.abstract_references import abstract_referance


class range_model(abstract_referance):
    __base = None
    __coef: int

    def __init__(self, name='', coef: int = 0, base = None):
        super().__init__(name)
        self.base = base
        self.coef = coef

    def convert_to_base(self, value):
        return value / self.coef if self.coef != 0 else 0

    def convert_from_base(self, value):
        return value * self.coef