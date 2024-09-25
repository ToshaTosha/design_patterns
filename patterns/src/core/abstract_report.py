from abc import ABC, abstractmethod
from src.core.format_reporting import format_reporting
from src.core.validator import validator

"""
Абстрактный класс для наследования для отчетов
"""


class abstract_report(ABC):
    __format: format_reporting = format_reporting.CSV
    __result: str = ""

    """
    Сформировать
    """

    @abstractmethod
    def create(self, data: list):
        pass

    """
    Тип формата
    """

    @property
    def format(self) -> format_reporting:
        return self.__format

    """
    Результат формирования отчета
    """

    @property
    def result(self) -> str:
        return self.__result

    @result.setter
    def result(self, value: str):
        validator.validate(value, str)
        self.__result = value

    def save_report(self, file_name):
        with open(file_name, "w") as file:
            file.write(self.result)

    def save(self, param):
        pass