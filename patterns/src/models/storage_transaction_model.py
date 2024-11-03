from datetime import datetime

from src.models.abstract_reference import abstract_reference
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model


class storage_transaction_model(abstract_reference):
    __storage: storage_model
    __nomenclature: nomenclature_model
    __period: datetime
    __quantity: float = 0.0
    __range: range_model
    __period: datetime
    __is_incoming: bool = True

    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        self.__storage = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        self.__range = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value

    @property
    def period(self) -> datetime:
        return self.__period

    @period.setter
    def period(self, value: datetime):
        self.__period = value

    @property
    def is_incoming(self) -> bool:
        return self.__is_incoming

    @is_incoming.setter
    def is_incoming(self, value: bool):
        self.__is_incoming = value

    @staticmethod
    def create(storage: storage_model, nomenclature: nomenclature_model,
               period: datetime, quantity: float, range: range_model, is_incoming: bool) -> 'storage_transaction_model':
        """Фабричный метод для создания экземпляра storage_transaction_model."""
        transaction = storage_transaction_model()
        transaction.storage = storage
        transaction.is_incoming = is_incoming
        transaction.nomenclature = nomenclature
        transaction.period = period
        transaction.quantity = quantity
        transaction.range = range
        return transaction

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)