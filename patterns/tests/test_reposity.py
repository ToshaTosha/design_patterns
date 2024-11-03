import unittest
from datetime import datetime
from src.models.storage_transaction_model import storage_transaction_model
from src.models.storage_model import storage_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model

class TestStorageTransactionModel(unittest.TestCase):

    def setUp(self):
        """Создаем необходимые объекты для тестирования."""
        self.storage = storage_model()
        self.storage.name = "Main Warehouse"
        self.storage.address = "123 Warehouse St."

        self.nomenclature = nomenclature_model()
        self.nomenclature.name = "Product A"

        self.range = range_model()
        self.range.name = "Unit"

        self.period = datetime.now()
        self.quantity = 100.0

    def test_create_storage_transaction(self):
        """Тестируем создание складской транзакции."""
        transaction = storage_transaction_model.create(
            storage=self.storage,
            nomenclature=self.nomenclature,
            period=self.period,
            quantity=self.quantity,
            range=self.range,
            is_incoming=True
        )

        # Проверяем, что транзакция создана правильно
        self.assertIsInstance(transaction, storage_transaction_model)
        self.assertEqual(transaction.storage, self.storage)
        self.assertEqual(transaction.nomenclature, self.nomenclature)
        self.assertEqual(transaction.period, self.period)
        self.assertEqual(transaction.quantity, self.quantity)
        self.assertEqual(transaction.range, self.range)

if __name__ == '__main__':
    unittest.main()
