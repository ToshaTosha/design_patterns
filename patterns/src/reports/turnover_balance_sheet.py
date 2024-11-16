from datetime import datetime
import matplotlib
matplotlib.use('Agg')
from src.core.abstract_logic import abstract_logic
from src.dto.observe_service import observe_service
from src.processes.process_storage_turn import process_storage_turn
from src import settings_manager
from src.core.format_reporting import format_reporting
from src.reports.report_factory import report_factory
import json

class turnover_balance_sheet(abstract_logic):
    def __init__(self, data, manager: settings_manager):
        observe_service.append(self)
        self.data = data
        self.manager = manager
        self._start_date = None
        self._end_date = None
        self._warehouse = ""
        print(self.manager.settings.block_period)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value: str):
        self._start_date = datetime.strptime(value, "%Y-%m-%d")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value: str):
        self._end_date = datetime.strptime(value, "%Y-%m-%d")

    @property
    def warehouse(self):
        return self._warehouse

    @warehouse.setter
    def warehouse(self, value: str):
        self._warehouse = value

    def calculate_osv(self, transactions: list):
        opening_turnovers, turnovers, receipts, consumptions = [], [], [], []
        process = process_storage_turn(self.manager)

        for transaction in transactions:
            if transaction.warehouse.name == self.warehouse:
                if transaction.period <= self.start_date:
                    opening_turnovers.append(transaction)

                if self.start_date <= transaction.period <= self.end_date:
                    turnovers.append(transaction)
                    (receipts if transaction.is_incoming else consumptions).append(transaction)

        opening_remainder = process.process(opening_turnovers)
        remainder = process.process(turnovers)
        return opening_remainder, receipts, consumptions, remainder

    def generate_report(self, request_data):
        self.start_date = request_data.get('start_date')
        self.end_date = request_data.get('end_date')
        self.warehouse = request_data.get('warehouse')

        opening_remainder, receipts, consumptions, remainder = self.calculate_osv(self.data)
        report_data = {
            "Opening Remainders": opening_remainder,
            "Remainders": remainder,
            "Receipts": receipts,
            "Consumptions": consumptions,
        }

        report = report_factory(self.manager).create(format_reporting.JSON)
        for key, result in report_data.items():
            report.create(result)
            report_data[key] = report.result

        self.save_report_to_file(report_data)
        return report_data

    def save_report_to_file(self, report_data):
        with open("osv.json", 'w', encoding='utf-8') as file:
            json.dump(report_data, file, ensure_ascii=False, indent=4)

    def set_exception(self, ex: Exception):
        return super().set_exception(ex)
