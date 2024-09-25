from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.core.validator import validator, operation_exception
from src.reports.json_report import json_report
from src.reports.markdown_report import markdown_report
from src.settings import Settings

"""
Фабрика для формирования отчетов
"""


class report_factory(abstract_logic):
    __reports = {}
    __settings = Settings()

    def __init__(self) -> None:
        super().__init__()
        # Наборы отчетов
        self.__reports[format_reporting.CSV] = csv_report
        self.__reports[format_reporting.MARKDOWN] = markdown_report
        self.__reports[format_reporting.JSON] = json_report

    """
    Получить инстанс нужного отчета
    """

    def create(self, format: format_reporting) -> abstract_report:
        validator.validate(format, format_reporting)

        if format not in self.__reports.keys():
            self.set_exception(operation_exception(f"Указанный вариант формата {format} не реализован!"))
            return None

        report = self.__reports[format]
        return report()

    def create_default(self) -> abstract_report:
        # Использование настроек для создания отчета по формату из настроек
        format_setting = self.__settings.report_format
        if format_setting not in self.__reports.keys():
            self.set_exception(
                operation_exception(f"Указанный вариант формата отчета {format_setting} не найден в настройках!"))
            return None

        report = self.__reports[format_setting]
        return report()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)