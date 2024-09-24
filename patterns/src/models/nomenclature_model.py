from src.exeptions import argument_exception
from src.models.abstract_reference import abstract_reference

class nomenclature_model(abstract_reference):
    __full_name:str = ''
    __group = None
    __range = None


    def __init__(self):
        super().__init__()

    @staticmethod
    def create_nomenclature(full_name, group):
        nom = nomenclature_model()
        nom.full_name = full_name
        nom.group = group
        return nom

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        if len(value) > 255:
            raise argument_exception('Full name should not exceed 255 characters')
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