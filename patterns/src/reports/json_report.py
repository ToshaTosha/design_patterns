from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception
import json

class json_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        json_data = []

        for item in data:
            json_item = {}
            for key, value in item.__dict__.items():
                if not key.startswith("_") and not callable(getattr(item, key)):
                    json_item[key] = value
            json_data.append(json_item)

        self.result = json.dumps(json_data, ensure_ascii=False, indent=4)
