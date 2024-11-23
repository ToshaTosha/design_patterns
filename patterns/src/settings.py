
"""
Настройки
"""
from datetime import datetime

from src.core.format_reporting import format_reporting
from src.core.event_type import event_type
from src.dto.observe_service import observe_service


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