from src.reports.json_report import json_report
from src.reports.markdown_report import markdown_report
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.settings_manager import SettingsManager as settings_manager

import unittest

"""
Набор тестов для проверки работы формирование отчетов
"""


class test_reporting(unittest.TestCase):
    """
    Проверка работы отчеиа CSV
    """

    def test_csv_report_create_range(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity, manager)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверки
        assert report.result != ""

    """
    Проверка работы отчеиа CSV
    """

    def test_csv_report_create_nomenclature(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity, manager)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверки
        assert report.result != ""

    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """

    def test_report_factory_create(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Действие
        report = report_factory().create(format_reporting.CSV)

        # Проверка
        assert report is not None
        assert isinstance(report, csv_report)


    def test_markdown_report_create_range(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity, manager)
        start.create()
        factory = report_factory()

        # Действие
        report = factory.create(format_reporting.MARKDOWN)
        report.create(reposity.data[data_reposity.range_key()])
        report.save("output_markdown_report")

        assert report is not None
        assert isinstance(report, markdown_report)

    def test_json_report_create_range(self):
        manager = settings_manager()
        manager.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity, manager)
        start.create()
        factory = report_factory()

        report = factory.create(format_reporting.JSON)
        report.create(reposity.data[data_reposity.range_key()])
        report.save("output_json_report")

        assert report is not None
        assert isinstance(report, json_report)