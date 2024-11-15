from datetime import datetime

import connexion

from src.core.event_type import event_type
from src.core.format_reporting import format_reporting
from src.dto.observe_service import observe_service
from src.models.nomenclature_model import nomenclature_model
from src.processes.process_factory import process_factory
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
from src.core.nomenclature_service import NomenclatureService

app = connexion.FlaskApp(__name__)

repository = data_reposity()
manager = settings_manager()
manager.open("settings.json")
start = start_service(repository, manager)
nomenclature_service_instance = NomenclatureService(repository)
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

    filter_data = request.get_json()

    # Извлекаем параметры фильтрации из запроса
    storage = filter_data.get("storage")
    nomenclature = filter_data.get("nomenclature")
    start_period = filter_data.get("start_period")
    end_period = filter_data.get("end_period")

    # Преобразуем строки в datetime, если они указаны
    if start_period:
        start_period = datetime.fromisoformat(start_period)
    if end_period:
        end_period = datetime.fromisoformat(end_period)

    prototype = domain_prototype(data)

    # Фильтруем данные на основе переданных параметров
    filtered_data = prototype.create(data, storage=storage, nomenclature=nomenclature, start_period=start_period,
                                     end_period=end_period)

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

        factory = process_factory()
        factory.build_structure(process_storage_turn)
        process = factory.create('storage_turn')
        turnovers = process.process(transactions=transactions)

        if not turnovers:
            return jsonify({"message": "No turnovers found"}), 404

        report = report_factory(manager).create(format_reporting.JSON)
        report.create(turnovers)

        return report.result
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/nomenclature', methods=['GET'])
def get_nomenclature():
    result = nomenclature_service_instance.get_nomenclature(request.args)
    if "error" in result or "status" in result:
        return jsonify(result), 404 if "error" in result else 200

    report = report_factory(manager).create(format_reporting.JSON)
    report.create(list(result))
    return report.result, 200

@app.route('/api/nomenclature', methods=['PUT'])
def add_nomenclature():
    result = nomenclature_service_instance.add_nomenclature(request.json)
    if not isinstance(result, nomenclature_model):
        return jsonify(result), 400

    report = report_factory(manager).create(format_reporting.JSON)
    report.create([result])
    return report.result, 201


@app.route('/api/nomenclature', methods=['PATCH'])
def update_nomenclature():
    statuses = observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, request.json)
    status = statuses[type(nomenclature_service_instance).__name__]
    return jsonify(status), 200

@app.route('/api/nomenclature', methods=['DELETE'])
def delete_nomenclature():
    try:
        statuses = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request.json)
        status = statuses[type(nomenclature_service_instance).__name__]
        return jsonify(status), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/settings/block_period', methods=['POST'])
def set_block_period():
    data = request.get_json()
    block_period_str = data.get('block_period')
    try:
        settings = manager.settings
        settings.block_period = block_period_str
        manager.save()
        return jsonify({"message": "Дата блокировки обновлена успешно."}), 200

    except (ValueError, AttributeError) as e:
        return jsonify({"error": "Неправильный формат даты или ошибка запроса.", "details": str(e)}), 400


@app.route('/settings/block_period', methods=['GET'])
def get_block_period():
    settings = manager.settings
    block_period_str = settings.block_period.strftime("%Y-%m-%d") if settings.block_period else None
    return jsonify({"block_period": block_period_str}), 200

if __name__ == '__main__':
    app.add_api('swagger.yaml')
    app.run(port=8080)
