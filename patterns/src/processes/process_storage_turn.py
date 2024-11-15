from datetime import datetime

from src import settings_manager
from src.models.storage_turn_model import storage_turn_model
from src.processes.abstract_process import abstract_process

class process_storage_turn(abstract_process):
    def __init__(self, manager: settings_manager = None, blocked_turnovers: dict = {}):
        self.block_period = manager.settings.block_period if manager else datetime.now()
        self.blocked_turnovers = blocked_turnovers

    def process(self, transactions: list) -> list:
        turnovers = {}

        for transaction in transactions:
            if transaction.period >= self.block_period:
                key = (
                    transaction.warehouse.unique_code,
                    transaction.nomenclature.unique_code,
                    transaction.range.unique_code
                )

                if key not in turnovers:
                    instance = storage_turn_model()
                    instance.storage=transaction.storage,
                    instance.nomenclature=transaction.nomenclature,
                    instance.range=transaction.range
                    turnovers[key] = instance

                if transaction.is_incoming:
                    turnovers[key].remains += transaction.quantity
                else:
                    turnovers[key].remains -= transaction.quantity
        for key, turnover in self.blocked_turnovers.items():
            if key in turnovers:
                turnovers[key].remains += turnover.turnover
            else:
                turnovers[key] = turnover

        return list(turnovers.values())
    