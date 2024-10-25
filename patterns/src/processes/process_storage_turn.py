from datetime import datetime
from src.processes.abstract_process import abstract_process

class process_storage_turn(abstract_process):
    def process(self, transactions: list) -> list:
        turnovers = {}

        for transaction in transactions:
            key = (transaction.storage.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)

            if key not in turnovers:
                turnovers[key] = {'turnover': 0.0}

            if transaction.is_incoming:
                turnovers[key]['turnover'] += transaction.quantity
            else:
                turnovers[key]['turnover'] -= transaction.quantity

        return [{'storage': k[0], 'nomenclature': k[1], 'range': k[2], 'turnover': v['turnover']} for k, v in turnovers.items()]