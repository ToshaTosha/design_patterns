import unittest
from datetime import datetime
from src.models.storage_model import storage_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_transaction_model import storage_transaction_model
from src.processes.process_storage_turn import process_storage_turn


class TestProcessStorageTurn(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.storage = storage_model()
        self.storage.name = "Склад 1"

        self.nomenclature = nomenclature_model()
        self.nomenclature.name = "Товар A"

        self.range = range_model()
        self.range.name = "Диапазон 1"

        self.transactions = [
            storage_transaction_model.create(self.storage, self.nomenclature, datetime(2023, 1, 1), 100, self.range,
                                             True),
            storage_transaction_model.create(self.storage, self.nomenclature, datetime(2023, 1, 5), -50, self.range,
                                             False),
            storage_transaction_model.create(self.storage, self.nomenclature, datetime(2023, 1, 10), 200, self.range,
                                             True),
            storage_transaction_model.create(self.storage, self.nomenclature, datetime(2023, 1, 15), -30, self.range,
                                             False),
            storage_transaction_model.create(self.storage, self.nomenclature, datetime(2023, 2, 1), 150, self.range,
                                             True),
        ]

    def test_process_storage_turn(self):
        process = process_storage_turn()
        result = process.process(self.transactions, storage=self.storage.name, start_period=datetime(2023, 1, 1),
                                 end_period=datetime(2023, 1, 31))

        expected_result = [
            {'storage': self.storage.unique_code, 'nomenclature': self.nomenclature.unique_code,
             'range': self.range.unique_code, 'turnover': 380.0}
        ]

        self.assertEqual(result, expected_result)

    def test_process_storage_turn_no_transactions(self):
        process = process_storage_turn()
        result = process.process([], storage=self.storage.name, start_period=datetime(2023, 1, 1),
                                 end_period=datetime(2023, 1, 31))

        expected_result = []

        self.assertEqual(result, expected_result)

    def test_process_storage_turn_with_different_storage(self):
        another_storage = storage_model()
        another_storage.name = "Склад 2"

        process = process_storage_turn()
        result = process.process(self.transactions, storage=another_storage.name, start_period=datetime(2023, 1, 1),
                                 end_period=datetime(2023, 1, 31))

        expected_result = []

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
