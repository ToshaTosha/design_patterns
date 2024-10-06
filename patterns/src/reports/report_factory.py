from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.core.validator import validator, operation_exception
from src.reports.json_report import json_report
from src.reports.markdown_report import markdown_report
from src.settings import Settings
from src.settings_manager import SettingsManager

"""
Фабрика для формирования отчетов
"""


class report_factory(abstract_logic):
    __reports: dict = {}
    __settings: dict = {}
    __settings_manager: SettingsManager = None

    def __init__(self, settings) -> None:
        super().__init__()
        self.__settings = settings
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

    def get_formats(self):
        for key, value in self.__settings_manager.settings.report_formats.items():
            self.reports_setting[format_reporting[key]] = value

    @property
    def reports(self) -> dict:
        return self.__reports

    @reports.setter
    def reports(self, value: dict):
        if not isinstance(value, dict):
            self.set_exception(operation_exception(f"Неверный формат!"))
            return None
        self.__reports = value

    @property
    def settings(self) -> Settings:
        return self.__settings_manager.settings

    @property
    def reports_setting(self) -> dict:
        return self.__settings

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)