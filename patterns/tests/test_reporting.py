import os

from src.reports.json_report import json_report
from src.reports.markdown_report import markdown_report
from src.reports.xml_report import xml_report
from src.settings import Settings
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

    def test_csv_reports(self):
        manager = settings_manager()
        repository = data_reposity()
        service = start_service(repository, manager)
        service.create()
        reports = {}

        nomenclature_report = csv_report()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report


        assert nomenclature_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.csv', 'w', encoding='utf-8') as f:
                f.write(value.result)

    def test_json_reports(self):
        manager = settings_manager()
        repository = data_reposity()
        service = start_service(repository, manager)
        service.create()
        reports = {}


        nomenclature_report = json_report()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report


        assert nomenclature_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.json', 'w', encoding='utf-8') as f:
                f.write(value.result)

    def test_markdown_reports(self):
        manager = settings_manager()
        repository = data_reposity()
        service = start_service(repository, manager)
        service.create()
        reports = {}

        nomenclature_report = markdown_report()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report


        assert nomenclature_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.md', 'w', encoding='utf-8') as f:
                f.write(value.result)

    def test_xml_reports(self):
        manager = settings_manager()
        repository = data_reposity()
        service = start_service(repository, manager)
        service.create()
        reports = {}

        nomenclature_report = xml_report()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        assert nomenclature_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.xml', 'w', encoding='utf-8') as f:
                f.write(value.result)