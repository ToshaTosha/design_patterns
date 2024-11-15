# -*- coding: utf-8 -*-

import json
import os
from src.core.abstract_logic import abstract_logic

from src.settings import Settings

"""
Менеджер настроек
"""

class SettingsManager(abstract_logic):
    __file_name = "settings.json"
    __settings: Settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting()

    def convert(self, data):
        if dict is None:
            raise TypeError("Некорректно переданы параметры!")
        for key, value in dict.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    """
    Открыть и загрузить настройки
    """

    def open(self, file_name: str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Некорректно переданы параметры!")

        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = os.path.relpath(self.__file_name)
            stream = open(full_name)
            data = json.load(stream)
            self.convert(data)

            return True

        except FileNotFoundError:
            self.__settings = self.__default_setting()
            return False
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.__settings = self.__default_setting()
            return False

    """
    Загруженные настройки
    """

    @property
    def settings(self):
        return self.__settings

    """
    Набор настроек по умолчанию
    """

    def __default_setting(self):
        data = Settings()
        data.inn = "380080920202"
        data.account = "58143369583"
        data.correspondent_account = "16557615117"
        data.bik = "876323279"
        data.business_type = "68339"
        data.block_period = "2024-01-01"
        data.report_formats = {
            "CSV": "CSVReport",
            "MARKDOWN": "MDReport",
            "JSON": "JSONReport"
        }

        return data

    def save(self):

        full_path = self.__get_file_path(self.__file_name)

        data_to_save = {
            "inn": self.__settings.inn,
            "account": self.__settings.account,
            "corr_account": self.__settings.correspondent_account,
            "bik": self.__settings.bik,
            "block_period": self.__settings.block_period
        }

        try:
            with open(full_path, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, ensure_ascii=False, indent=4)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.set_exception(e)
            raise "Ошибка при сохранении данных в файл."

    @staticmethod
    def __get_file_path(filename, search_path=os.curdir):
        for root, dirs, files in os.walk(search_path):
            full_path = os.path.join(root, filename)
            if os.path.isfile(full_path):
                return full_path
        return None

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
