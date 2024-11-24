
"""
Настройки
"""
from datetime import datetime

from src.core.format_reporting import format_reporting
from src.core.event_type import event_type
from src.dto.observe_service import observe_service

from src.core.logging import LogType
from src.exeptions import ArgumentTypeException, UnknownValueException


class Settings:
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bik = ""
    __business_type = ""
    __report_format = ""
    __report: format_reporting = format_reporting.CSV
    __block_period = ""
    __report_formats= {}
    __min_log_type: LogType = LogType.DEBUG
    __log_to_console: bool = True
    __log_to_file: bool = True
    __log_file_path: str = "../log.txt"

    report_formats_mapping = {
        "CSV": "csv_report",
        "Markdown": "markdown_report",
        "Json": "json_report",
        "XML": "xml_report",
        "RTF": "rtf_report"
    }

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting INN"})
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 12:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting INN"})
            raise ValueError("Номер ИНН должен быть 12 символов")

        self.__inn = value
        observe_service.raise_event(event_type.INFO, {"message": f"INN set to: {value}"})

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting account"})
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 11:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting account"})
            raise ValueError("Номер счёта должен быть 11 символов")
        observe_service.raise_event(event_type.INFO, {"message": f"Account set to: {value}"})
        self.__account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен быть 11 символов")
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 9:
            raise ValueError("БИК должен быть 9 символов")
        self.__bik = value

    @property
    def business_type(self):
        return self.__business_type

    @business_type.setter
    def business_type(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 5:
            raise ValueError("Вид собственности должен быть 5 символов")
        self.__business_type = value

    @property
    def block_period(self):
        return self.__block_period

    @block_period.setter
    def block_period(self, value: str):
        self.__block_period = datetime.strptime(value, "%Y-%m-%d")

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: str):
        if value not in self.report_formats_mapping:
            raise ValueError(f"Неподдерживаемый формат отчета: {value}")
        self.__report_format = value

    def get_report_class(self):
        return self.report_formats_mapping.get(self.__report_format, "default_report_class")

    @property
    def log_file_path(self) -> str:
        return self.__log_file_path

    @log_file_path.setter
    def log_file_path(self, value: str):
        if not isinstance(value, str):
            observe_service.raise_event(event_type.ERROR, ArgumentTypeException('log_file_path', "str"))
            ArgumentTypeException('log_file_path', "str")
        observe_service.raise_event(event_type.DEBUG, f"Путь до файла логирования {value}")
        self.__log_file_path = value

    @property
    def log_to_file(self):
        return self.__log_to_file

    @log_to_file.setter
    def log_to_file(self, value: str):
        if not isinstance(value, str):
            observe_service.raise_event(event_type.ERROR, ArgumentTypeException('log_to_file', "str"))
            raise ArgumentTypeException("log_to_file", "str")
        if value == "True":
            observe_service.raise_event(event_type.DEBUG, f"Логирование в файл разешено")
            self.__log_to_file = True
        elif value == "False":
            observe_service.raise_event(event_type.DEBUG, f"Логирование в файл запрещено")
            self.__log_to_file = False
        else:
            observe_service.raise_event(event_type.ERROR, "Неизвестные данные для log_to_file")
            raise UnknownValueException()

    @property
    def log_to_console(self):
        return self.__log_to_console

    @log_to_console.setter
    def log_to_console(self, value: str):
        if not isinstance(value, str):
            observe_service.raise_event(event_type.ERROR, ArgumentTypeException('log_to_console', "str"))
            raise ArgumentTypeException("log_to_console", "str")
        if value == "True":
            observe_service.raise_event(event_type.DEBUG, f"Логирование в консоль разешено")
            self.__log_to_console = True
        elif value == "False":
            observe_service.raise_event(event_type.DEBUG, f"Логирование в консоль запрещено")
            self.__log_to_console = False
        else:
            observe_service.raise_event(event_type.ERROR, "Неизвестные данные для log_to_console")
            raise UnknownValueException()

    @property
    def min_log_type(self) -> LogType:
        return self.__min_log_type

    @min_log_type.setter
    def min_log_type(self, value: int):
        if not isinstance(value, int):
            observe_service.raise_event(event_type.ERROR, ArgumentTypeException('min_log_type', "int"))
            ArgumentTypeException('min_log_type', "int")
        for type in LogType:
            if type.value == value:
                observe_service.raise_event(event_type.DEBUG,
                                           f"Минимальный уровень логирования {type.value} ({type.name})")
                self.__min_log_type = type