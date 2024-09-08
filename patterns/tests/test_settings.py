import unittest

from src.settings_manager import SettingsManager

class TestSettings(unittest.TestCase):

    def test_open(self):
        manager = SettingsManager()

        self.assertTrue(manager.open("../settings.json"))
        self.assertTrue(manager.open("test_settings.json"))

class TestSettingsManager(unittest.TestCase):
    def test_settings_loading(self):
        manager = SettingsManager()
        result = manager.open("../settings.json")
        self.assertTrue(result)
        self.assertEqual(manager.settings.inn, "380930934900")
        self.assertEqual(manager.settings.account, "58143369583")
        self.assertEqual(manager.settings.correspondent_account, "16557615117")
        self.assertEqual(manager.settings.bik, "876323279")
        self.assertEqual(manager.settings.business_type, "68339")
