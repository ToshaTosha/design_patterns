from src.models.abstract_reference import abstract_reference
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.storage_model import storage_model


class storage_turn_model(abstract_reference):
    __storage: storage_model
    __remains: int
    __nomenclature: nomenclature_model
    __range: range_model

    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        self.__storage = value

    @property
    def remains(self) -> int:
        return self.__remains

    @remains.setter
    def remains(self, value: int):
        self.__remains = value

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

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)