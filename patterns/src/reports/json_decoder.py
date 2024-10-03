import importlib
import inspect
import pkgutil
import sys
from json import JSONDecoder

from src.core.validator import operation_exception


class JsonModelDecoder(JSONDecoder):

    def __init__(self):
        super().__init__()
        self.classes = {}
        for sub_module in sys.modules:
            if sub_module.startswith("src.models"):
                sub_module_obj = sys.modules[sub_module]
                self.classes.update({name: cls for name, cls in inspect.getmembers(sub_module_obj, inspect.isclass)})

    def decode(self, s, _w=None):
        if isinstance(s, str):
            decoded_content = self.raw_decode(s)[0]
        else:
            decoded_content = s

        model_key = decoded_content.get("cls") or list(decoded_content.keys())[0]
        cls = self.classes.get(model_key)

        if cls is None:
            raise operation_exception("Неизвестный набор данных")

        data = decoded_content.get(model_key) or decoded_content[model_key]
        if isinstance(data, list):
            models = [self.decode_model(item, cls) for item in data]
        else:
            models = self.decode_model(data, cls)

        return models

    def decode_model(self, coded_obj, cls):
        model = cls()
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(model, x)), dir(model)))

        for field in fields:
            if field not in coded_obj:
                continue
            value = coded_obj[field]
            if isinstance(value, dict) and "cls" in value:
                nested_cls_name = value["cls"]
                nested_cls = self.classes.get(nested_cls_name)
                if nested_cls:
                    value = self.decode_model(value, nested_cls)
            setattr(model, field, value)
        return model