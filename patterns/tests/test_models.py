import unittest

from src.models.range_model import range_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.organization_model import organization_model
from src.settings_manager import SettingsManager


class test_models(unittest.TestCase):

    def test_range_model_creation(self):
        base_range = range_model("грамм")
        base_range.coef = 1
        self.assertEqual(base_range.name, "грамм")
        self.assertEqual(base_range.coef, 1)

    def test_range_conversion(self):
        base_range = range_model("грамм")
        new_range = range_model("кг")
        new_range.coef = 1000
        new_range.base = base_range

        gram_in_kilo = new_range.to_base

        self.assertEqual(gram_in_kilo.name, 'грамм')
        self.assertEqual(gram_in_kilo.base, None)

    def test_range_model_compare_mode(self):
        range1 = range_model("range1")
        range2 = range_model("range1")

        self.assertTrue(range1.set_compare_mode(range2))

        range3 = range_model("range3")
        self.assertFalse(range1.set_compare_mode(range3))

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
        base_range = range_model("грамм")
        nom = nomenclature_model("nomen")
        nom.full_name = "full_name"
        nom.group = group
        nom.range = base_range

        self.assertEqual(nom.name, "nomen")
        self.assertEqual(nom.group, group)
        self.assertEqual(nom.range, base_range)
        self.assertEqual(nom.full_name, "full_name")

