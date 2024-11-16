import json
import os
from src.data_reposity import data_reposity
from src.core.abstract_logic import abstract_logic
from src import settings_manager
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.dto.observe_service import observe_service

class reposity_manager(abstract_logic):
    def __init__(self, repository: data_reposity, manager: settings_manager, file_path: str = "repository_data.json"):
        self.repository = repository
        self.file_path = file_path
        self.manager = manager
        observe_service.append(self)

    def save_to_file(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                report = report_factory(self.manager).create(format_reporting.JSON)
                data_to_save = {key: report.create(item).result for key, item in self.repository.data.items()}
                json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении данных в файл: {e}")

    def restore_from_file(self):
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError("Файл данных не найден. Пожалуйста, сохраните данные перед восстановлением.")

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data_loaded = json.load(file)
                for key, item_data in data_loaded.items():
                    item_data = json.loads(item_data) if isinstance(item_data, str) else item_data
                    item_instance = self.repository.create_item(key)
                    self.repository.data[key] = [item_instance().deserialize(item) for item in item_data]
            print("Данные успешно восстановлены из файла.")
        except Exception as e:
            raise RuntimeError(f"Ошибка при восстановлении данных из файла: {e}")

    def set_file_path(self, new_path: str):
        self.file_path = new_path

    def set_exception(self, ex: Exception):
        return super().set_exception(ex)
