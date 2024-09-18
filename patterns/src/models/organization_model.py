from src.models.abstract_reference import abstract_reference

class organization_model(abstract_reference):
    __inn:str = ''
    __bik:str = ''
    __account:str = ''
    __business_type:str = ''


    def __init__(self):
        super().__init__()

    @property
    def inn(self):
        return self.__inn

    @property
    def bik(self):
        return self.__bik

    @property
    def account(self):
        return self.__account

    @property
    def business_type(self):
        return self.__business_type

    def initialize_settings(self, settings_manager):
        self.__inn = settings_manager.inn
        self.__bik = settings_manager.bik
        self.__account = settings_manager.account
        self.__business_type = settings_manager.business_type

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)