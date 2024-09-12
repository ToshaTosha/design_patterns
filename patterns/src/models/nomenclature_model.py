from src.exeptions import argument_exception
from src.models.abstract_references import abstract_referance
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.range_model import range_model

class nomenclature_model(abstract_referance):
    __full_name:str = ''
    __group = None
    __range = None


    def __init__(self, name: str, group: nomenclature_group_model, range: range_model, full_name: str = ''):
        super().__init__(name)

        if len(full_name) > 255:
            raise argument_exception('Full name should not exceed 255 characters')

        self.full_name = full_name
        self.range = range
        self.group = group