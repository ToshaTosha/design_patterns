from src.core.abstract_logic import abstract_logic
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.storage_model import storage_model
from src.models.storage_transaction_model import storage_transaction_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.storage_turn_model import storage_turn_model

"""
Репозиторий данных
"""


class data_reposity(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_reposity, cls).__new__(cls)
        return cls.instance

    """
    Набор данных
    """

    @property
    def data(self):
        return self.__data

    """
    Ключ для хранения групп номенклатуры
    """

    @staticmethod
    def group_key() -> str:
        return "group_key"

    @staticmethod
    def nomenclature_key() -> str:
        return 'nomenclature_key'

    @staticmethod
    def range_key() -> str:
        return 'range_key'

    @staticmethod
    def recipe_key():
        return 'recipe_key'

    @staticmethod
    def transactions_key() -> str:
        return "transactions"

    @staticmethod
    def keys() -> dict:
        result = {}
        methods = [method for method in dir(data_reposity) if
                   callable(getattr(data_reposity, method)) and method.endswith('_key')]

        for method in methods:
            key_name = method.replace('_key', '')
            key_value = getattr(data_reposity, method)()
            result[key_name] = key_value

        return result

    @staticmethod
    def create_item(key):
        model_mapping = {
            "nomenclature": nomenclature_model,
            "warehouses": storage_model,
            "range": range_model,
            "group": nomenclature_group_model,
            "recipes": recipe_model,
            "transactions": storage_transaction_model,
            "turnovers": storage_turn_model
        }
        model_class = model_mapping.get(key)
        if model_class:
            return model_class
        else:
            raise ValueError(f"Неизвестный ключ: {key}. Невозможно создать объект.")

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
