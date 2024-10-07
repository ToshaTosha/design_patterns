import connexion
from flask import Response

from src.core.format_reporting import format_reporting
from src.reports import report_factory
from src.core.validator import operation_exception, validator
from src.data_reposity import data_reposity
from src.settings_manager import SettingsManager as settings_manager
from src.start_service import start_service
from src.reports.report_factory import report_factory
from src.reports.json_report import json_report

app = connexion.FlaskApp(__name__)

repository = data_reposity()
manager = settings_manager()
manager.open("settings.json")
start = start_service(repository, manager)
start.create()

"""
Получить список форматов отчетов
"""


@app.route("/api/reports/formats", methods=['GET'])
def formats():
    result = []
    for report in format_reporting:
        result.append({"name": report.name, "value": report.value})

    return result


@app.route("/api/reports/<category>", methods=["GET"])
def get_report(category):
    data = {
        'nomenclature': repository.nomenclature_key(),
        'nomenclature_group': repository.group_key(),
        'range': repository.range_key(),
        'recipe': repository.recipe_key()
    }

    if category not in data:
        raise ValueError("Указанная категория данных отсутствует!")

    try:
        report = json_report()
        report.create(repository.data[data[category]])
    except:
        raise ValueError("Указанный формат отчёта отсутствует!")

    return report.result, 200


if __name__ == '__main__':
    app.add_api('swagger.yaml')
    app.run(port=8080)
