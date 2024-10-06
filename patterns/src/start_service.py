from src.core.abstract_logic import abstract_logic
from src.data_reposity import data_reposity
from src.core.validator import validator
from src.models.recipe_model import recipe_model, receipt_row
from src.settings_manager import SettingsManager as settings_manager
from src.settings import Settings as settings
from src.models.range_model import range_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nomenclature_group_model import nomenclature_group_model

"""
Сервис для реализации первого старта приложения
"""
class start_service(abstract_logic):
    __reposity: data_reposity = None
    __settings_manager: settings_manager = None

    def __init__(self, reposity: data_reposity, manager: settings_manager ) -> None:
        super().__init__()
        validator.validate(reposity, data_reposity)
        validator.validate(manager, settings_manager)
        self.__reposity = reposity
        self.__settings_manager = manager

    """
    Текущие настройки
    """
    @property
    def settings(self) -> settings:
        return self.__settings_manager.settings


    def __create_nomenclature_data(self):
        list = []
        recipe = self.__reposity.data[data_reposity.recipe_key()]
        for recipe in self.__reposity.data[data_reposity.recipe_key()]:
            for ingredient in recipe.rows:
                if ingredient.nomenclature not in list:
                    list.append(ingredient.nomenclature)
        self.__reposity.data[data_reposity.nomenclature_key()] = list

    def __create_measurement_units_data(self):
        nomens = self.__reposity.data[data_reposity.nomenclature_key()]
        print(list(set([x.range for x in nomens])))
        self.__reposity.data[data_reposity.range_key()] = list(set([x.range for x in nomens]))

    def __create_nomenclature_group(self):
        nomens = self.__reposity.data[data_reposity.nomenclature_key()]
        self.__reposity.data[data_reposity.group_key()] = list(set([x.group for x in nomens]))

    def __create_recipets(self):
        list = []
        recipe = recipe_model()
        nomen_group = nomenclature_group_model.default_group_source()

        range_gramm = range_model.create_gramm()
        range_count = range_model.create_count()

        data = []

        ingredients = [
            {"name": "Пшеничная мука", "full_name": "Пшеничная мука", "value": 100, "range": range_gramm},
            {"name": "Сахар", "full_name": "Сахар", "value": 50, "range": range_gramm},
            {"name": "Сливочное масло", "full_name": "Сливочное масло", "value": 40, "range": range_gramm},
            {"name": "Яйца", "full_name": "Яйца", "value": 1, "range": range_count}
        ]

        for ingredient in ingredients:
            nom = nomenclature_model.create_nomenclature(ingredient["full_name"], nomen_group, ingredient["range"])

            row = receipt_row()
            row.nomenclature = nom
            row.range = range_count
            row.value = ingredient["value"]

            data.append(row)

        recipe.name = 'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ'
        print('data', data)
        recipe.rows = data
        recipe.description = '''
            Для приготовления вкусных вафель смешайте пшеничную муку с сахаром, растопленным сливочным маслом и взбитыми яйцами.
            Готовьте вафли в разогретой вафельнице до золотистости. Подавайте горячие вафли с добавлением свежих фруктов, меда или сиропа по вкусу.
        '''

        list.append(recipe)

        self.__reposity.data[data_reposity.recipe_key()] = list

    def create(self):
        self.__create_recipets()
        self.__create_nomenclature_data()
        self.__create_nomenclature_group()
        self.__create_measurement_units_data()
        result = list(self.__reposity.data.values())

        return result


    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    @property
    def reposity(self):
        return self.__reposity