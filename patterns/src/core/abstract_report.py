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

    @staticmethod
    def get_class_fields(class_object: object):
        return list(filter(lambda x: not x.startswith("_") and not callable(getattr(class_object.__class__, x)),
                           dir(class_object.__class__)))

    def save_report(self, file_name):
        try:
            # Проверка наличия файла
            with open(file_name, "x", encoding="utf-8") as file:
                file.write(self.result)
                return True
        except FileExistsError:
            print("Файл уже существует. Пожалуйста, выберите другое имя файла.")
        except PermissionError:
            print("У вас нет прав на запись в этот файл.")
        except Exception as e:
            print(f"Произошла ошибка при записи файла: {e}")
        return False

    def save(self, param):
        pass