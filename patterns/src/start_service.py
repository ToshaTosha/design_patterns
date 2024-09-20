from src.core.abstract_logic import abstract_logic
from src.data_reposity import data_reposity
from src.core.validator import validator
from src.models.nomenclature_group_model import nomenclature_group_model as group_model
from src.models.recipe_model import recipe_model
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
        self.__reposity.data[data_reposity.nomenclature_key()] = self.__reposity.data[data_reposity.recipe_key()].noms

    def __create_measurement_units_data(self):
        nomens = self.__reposity.data[data_reposity.nomenclature_key()]
        self.__reposity.data[data_reposity.group_key()] = list(set([x.group for x in nomens]))

    def __create_nomenclature_group(self):
        nomens = self.__reposity.data[data_reposity.nomenclature_key()]
        self.__reposity.data[data_reposity.range_key()] = list(set([x.group for x in nomens]))

    def __create_recipets(self):
        recipe = recipe_model()
        nomen_group = nomenclature_group_model.default_group_source()
        data = []

        nom = nomenclature_model()
        nom.name = 'Пшеничная мука'
        nom.full_name = 'Пшеничная мука'
        nom.group = nomen_group
        data.append(nom)

        nom = nomenclature_model()
        nom.name = 'Сахар'
        nom.full_name = 'Сахар'
        nom.group = nomen_group
        data.append(nom)

        nom = nomenclature_model()
        nom.name = 'Сливочное масло'
        nom.full_name = 'Сливочное масло'
        nom.group = nomen_group
        data.append(nom)

        nom = nomenclature_model()
        nom.name = 'Яйца'
        nom.full_name = 'Яйца'
        nom.group = nomen_group
        data.append(nom)
        recipe.name = 'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ'
        recipe.noms = data
        recipe.description = '''
            Для приготовления вкусных вафель смешайте пшеничную муку с сахаром, растопленным сливочным маслом и взбитыми яйцами.
            Готовьте вафли в разогретой вафельнице до золотистости. Подавайте горячие вафли с добавлением свежих фруктов, меда или сиропа по вкусу.
        '''

        self.__reposity.data[data_reposity.recipe_key()] = recipe

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