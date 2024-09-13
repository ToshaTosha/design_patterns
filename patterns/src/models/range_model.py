from src.models.abstract_reference import abstract_reference


class range_model(abstract_reference):
    __base = None
    __coef: int = 0

    def __init__(self):
        super().__init__()

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        self.__base = value

    @property
    def coef(self):
        return self.__coef

    @coef.setter
    def coef(self, value):
        self.__coef = value


    @property
    def to_base(self):
        if self.base is None:
            return self
        return self.base

    def set_compare_mode(self, other_object) -> bool:
        result = super().set_compare_mode(other_object)
        return result