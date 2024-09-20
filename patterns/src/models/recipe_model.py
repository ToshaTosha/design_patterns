from src.exeptions import argument_exception
from src.models.range_model import range_model
from src.models.abstract_reference import abstract_reference
from src.models.nomenclature_model import nomenclature_model


class receipt_row(abstract_reference):
    __nomenclature: nomenclature_model = None
    __range: range_model = None
    __value: float = 0

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        self.__nomenclature = value

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        self.__range = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

class recipe_model(abstract_reference):
    __name: str
    __rows: list[receipt_row]
    __description: str

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def noms(self):
        return self.__noms

    @noms.setter
    def noms(self, value):
        self.__noms = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)