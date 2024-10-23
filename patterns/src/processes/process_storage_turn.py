from datetime import datetime
from src.processes.abstract_process import abstract_process

class process_storage_turn(abstract_process):
    def process(self, transactions: list, storage: str, nomenclature: str = None,
                start_period: datetime = None, end_period: datetime = None) -> list:
        turnovers = {}

        for transaction in transactions:
            if start_period and not (start_period <= transaction.period <= end_period):
                continue
            if storage and transaction.storage.name != storage:
                continue
            if nomenclature and transaction.nomenclature.name != nomenclature:
                continue

            key = (transaction.storage.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)

            if key not in turnovers:
                turnovers[key] = {'turnover': 0.0}

            if transaction.is_incoming:
                turnovers[key]['turnover'] += transaction.quantity
            else:
                turnovers[key]['turnover'] -= transaction.quantity

        return [{'storage': k[0], 'nomenclature': k[1], 'range': k[2], 'turnover': v['turnover']} for k, v in turnovers.items()]