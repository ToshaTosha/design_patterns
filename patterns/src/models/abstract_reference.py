from abc import ABC, abstractmethod
import uuid
from src.exeptions import argument_exception

class abstract_reference(ABC):
    __unique_code: uuid.UUID
    __name: str = ''

    def __init__(self, name: str = ''):
        if len(name) > 50:
            raise argument_exception('Name should not exceed 50 characters')
        self.name = name
        self.__id = str(uuid.uuid4())

    """
    Уникальный код
    """
    @property
    def unique_code(self) -> str:
        return self.__name

    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is None: return False
        if not isinstance(other_object, abstract_reference): return False

        return self.name == other_object.name