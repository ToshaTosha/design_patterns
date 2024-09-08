# -*- coding: utf-8 -*-

from src.settings_manager import SettingsManager

manager = SettingsManager()
manager.open("settings.json")
print(manager.settings.inn)
