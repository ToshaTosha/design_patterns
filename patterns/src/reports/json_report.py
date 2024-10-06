from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception
import json


class JsonModelEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            result = {}
            for k, v in o.__dict__.items():
                key = k.split('__')[-1]
                key = key.lstrip('_')
                result[key] = v
            return result
        return super().default(o)

class json_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        first_model = data[0]
        # список полей
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)),
                             dir(first_model)))

        result = {}
        lst = []
        for row in data:
            item = {}
            for field in fields:
                value = getattr(row, field)
                item[field] = value
            lst.append(item)
        result[type(first_model).__name__] = lst
        self.result = json.dumps(result, cls=JsonModelEncoder, indent=2)
