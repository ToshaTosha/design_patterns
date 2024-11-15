from src import settings_manager
from src.models.storage_turn_model import storage_turn_model
from src.processes.abstract_process import abstract_process


class storage_turnover_blocked_process(abstract_process):
    def __init__(self, manager: settings_manager):
        self.manager = manager
        self.block_period = self.manager.settings.block_period

    def process(self, transactions) -> list:
        turnovers = {}

        for transaction in transactions:
            if transaction.period > self.block_period:
                continue

            key = (
            transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)

            if key not in turnovers:
                instance = storage_turn_model()
                instance.storage = transaction.storage,
                instance.nomenclature = transaction.nomenclature,
                instance.range = transaction.range
                turnovers[key] = instance

            if transaction.is_incoming:
                turnovers[key].remains += transaction.quantity
            else:
                turnovers[key].remains -= transaction.quantity
        return turnovers