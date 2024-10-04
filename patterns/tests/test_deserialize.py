import os
import unittest

from src.data_reposity import data_reposity
from src.models.nomenclature_model import nomenclature_model
from src.reports.json_decoder import JsonModelDecoder
from src.reports.json_report import json_report
from src.start_service import start_service
from src.settings_manager import SettingsManager as settings_manager


class test_deserialize(unittest.TestCase):
    def test_json_reports(self):
        manager = settings_manager()
        repository = data_reposity()
        service = start_service(repository, manager)
        service.create()
        reports = {}

        nomenclature_report = json_report()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.json', 'w', encoding='utf-8') as f:
                f.write(value.result)

        with open(f'reports/{key}.json', 'r', encoding='utf-8') as f:
            result = JsonModelDecoder().decode(f.read())
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(nomenclature_model, x)),
                             dir(nomenclature_model)))
        nomenclature = repository.data[repository.nomenclature_key()]

        passed = 0
        for i in range(len(result)):
            assert isinstance(result[i], nomenclature_model)
            if result[i] == nomenclature[i]:
                passed += 1
                for field in fields:
                    assert getattr(result[i], field) == getattr(nomenclature[i], field)