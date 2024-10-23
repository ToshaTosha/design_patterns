from src.dto.filter_type import filter_type
from src.core.abstract_logic import abstract_logic

class filter_dto(abstract_logic):
    def __init__(self, name: str = "", unique_code: str = "", type: filter_type = filter_type.EQUALS):
        self.__name: str = name
        self.__unique_code: str = unique_code
        self.__type: filter_type = type

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value