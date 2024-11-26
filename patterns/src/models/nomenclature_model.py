from src.exeptions import ArgumentMaxLengthException
from src.models.abstract_reference import abstract_reference
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model


class nomenclature_model(abstract_reference):
    __full_name:str = ''
    __range = None
    __group: nomenclature_group_model = None


    def __init__(self):
        super().__init__()

    @staticmethod
    def create_nomenclature(full_name:str, range:range_model, group: nomenclature_group_model) -> 'nomenclature_model':
        nom = nomenclature_model()
        nom.full_name = full_name
        nom.group = group
        nom.range = range
        return nom

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        if len(value) > 255:
            raise ArgumentMaxLengthException("name", 255)
        self.__full_name = value

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        self.__range = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)
