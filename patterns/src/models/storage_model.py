from src.models.abstract_reference import abstract_reference


class storage_model(abstract_reference):
    __name: str = ""
    __address: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value.strip()

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value.strip()

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)