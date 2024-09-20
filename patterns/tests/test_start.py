from src.settings_manager import SettingsManager as settings_manager
from src.start_service import start_service
from src.data_reposity import data_reposity
import unittest


class test_settings(unittest.TestCase):

    def test_create_start_service(self):
        manager = settings_manager()
        manager.open("../settings.json")
        reposity = data_reposity()

        start = start_service(reposity, manager)

        result = start.create()

        assert len(result) > 0
        assert start.reposity is not None
        assert reposity.nomenclature_key() in reposity.data
        assert reposity.group_key() in reposity.data
        assert reposity.range_key() in reposity.data
        assert reposity.recipe_key() in reposity.data