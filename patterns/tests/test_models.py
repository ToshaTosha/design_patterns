import unittest

from src.models.range_model import range_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.organization_model import organization_model
from src.settings_manager import SettingsManager


class test_models(unittest.TestCase):

    def test_range_model_creation(self):
        base_range = range_model("грамм", 1)
        self.assertEqual(base_range.name, "грамм")
        self.assertEqual(base_range.coef, 1)

    def test_unit_conversion(self):
        base_range = range_model("грамм", 1)
        new_range = range_model("кг", 1000, base_range)

        value = 1500
        base_value = new_range.convert_to_base(value)
        self.assertEqual(base_value, value / 1000)

        value = 2.5
        converted_value = new_range.convert_from_base(value)
        self.assertEqual(converted_value, value * 1000)

    def test_organizations(self):
        manager = SettingsManager()
        manager.open('../settings.json')
        organ = organization_model(manager.settings, 'org')

        self.assertEqual(organ.inn, "380930934900")
        self.assertEqual(organ.account, "58143369583")
        self.assertEqual(organ.bik, "876323279")
        self.assertEqual(organ.business_type, "68339")

    def test_nomen(self):
        group = nomenclature_group_model('group')
        base_range = range_model("грамм", 1)
        nom = nomenclature_model("nomen", group, base_range, "full_name")

        self.assertEqual(nom.name, "nomen")
        self.assertEqual(nom.group, group)
        self.assertEqual(nom.range, base_range)
        self.assertEqual(nom.full_name, "full_name")

