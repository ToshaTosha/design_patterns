from src.models.abstract_reference import abstract_reference

class organization_model(abstract_reference):
    __inn:str = ''
    __bik:str = ''
    __account:str = ''
    __business_type:str = ''


    def __init__(self, settings_manager, name: str = ''):
        super().__init__(name)
        self.inn = settings_manager.inn
        self.bik = settings_manager.bik
        self.account = settings_manager.account
        self.business_type = settings_manager.business_type

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)