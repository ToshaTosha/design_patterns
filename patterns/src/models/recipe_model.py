from src.models.abstract_reference import abstract_reference
from src.models.receipt_row import receipt_row


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