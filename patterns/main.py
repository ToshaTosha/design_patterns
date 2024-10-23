import connexion
from flask import Response

from src.core.format_reporting import format_reporting
from src.processes.process_storage_turn import process_storage_turn
from src.reports import report_factory
from src.data_reposity import data_reposity
from src.settings_manager import SettingsManager as settings_manager
from src.start_service import start_service
from src.reports.report_factory import report_factory
from src.reports.json_report import json_report
from flask import jsonify, request
from src.dto.domain_prototype import domain_prototype
from src.dto.filter_dto import filter_dto

app = connexion.FlaskApp(__name__)

repository = data_reposity()
manager = settings_manager()
manager.open("settings.json")
start = start_service(repository, manager)
start.create()

data_mapping = repository.keys()

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

@app.route("/api/filter/<domain_type>", methods=["POST"])
def filter_data(domain_type):
    if domain_type not in data_mapping:
        return jsonify({"error": "Invalid domain type"}), 400

    filter_data = request.get_json()
    try:
        filt = filter_dto.from_dict(filter_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    data = repository.data[data_mapping[domain_type]]
    if not data:
        return jsonify({"error": "No data available"}), 404
    prototype = domain_prototype(data)
    filtered_data = prototype.create(data, filt)
    if not filtered_data.data:
        return jsonify({"message": "No data found"}), 404

    report = report_factory(manager).create(format_reporting.JSON)
    report.create(filtered_data.data)

    return report.result

@app.route("/api/filter/transactions", methods=["POST"])
def get_transactions():
    data = repository.data[data_mapping[data_reposity.transactions_key()]]
    if not data:
        return jsonify({"error": "No data available"}), 404

    prototype = domain_prototype(data)

    filtered_data = prototype.create(data)

    if not filtered_data.data:
        return jsonify({"message": "No transactions found"}), 404

    report = report_factory(manager).create(format_reporting.JSON)
    report.create(filtered_data.data)
    return report.result

@app.route("/api/filter/turnover", methods=["POST"])
def get_turnover():
    try:
        transactions = repository.data[data_reposity.transactions_key()]

        if not transactions:
            return jsonify({"error": "No transactions available"}), 404

        process = process_storage_turn()

        turnovers = process.process(transactions=transactions)

        if not turnovers:
            return jsonify({"message": "No turnovers found"}), 404

        report = report_factory(manager).create(format_reporting.JSON)
        report.create(turnovers)

        return report.result
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.add_api('swagger.yaml')
    app.run(port=8080)
