from abc import ABC, abstractmethod
import uuid
from src.exeptions import argument_exception

class abstract_referance(ABC):
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
        return self.__unique_code
