from abc import ABC, abstractmethod
import uuid
from src.exeptions import argument_exception

class abstract_reference(ABC):
    __unique_code: str
    __name: str = ''

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) > 50:
            raise ValueError('Name should not exceed 50 characters')
        self.__name = value

    """
    Уникальный код
    """
    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value):
        self.__unique_code = value

    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is None: return False
        if not isinstance(other_object, abstract_reference): return False

        return self.name == other_object.name