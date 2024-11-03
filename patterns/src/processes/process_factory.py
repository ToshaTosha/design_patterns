from src.processes.abstract_process import abstract_process
from src.processes.process_storage_turn import process_storage_turn


class process_factory:
    def __init__(self):
        self.__processes = {}

    def build_structure(self, process_class):
        self.__processes['storage_turn'] = process_class

    def create(self, process_name: str) -> abstract_process:
        process_class = self.__processes.get(process_name)
        if not process_class:
            raise ValueError(f"Процесс '{process_name}' не зарегистрирован.")
        return process_class()