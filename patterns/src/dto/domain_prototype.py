from src.core.abstract_prototype import abstract_prototype
from src.models.abstract_reference import abstract_reference
from src.dto.filter_dto import filter_dto
from src.dto.filter_type import filter_type
from src.dto.filter_matcher import filter_matcher
from src.core.validator import validator, argument_exception, operation_exception

class domain_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)
        self.matcher = filter_matcher()

    def create(self, data: list, filt: filter_dto):
        validator.validate_not_none(data, 'data')
        validator.validate_not_none(filt, 'filt')

        self.data = self.filter_by_field(data, filt, 'name')
        self.data = self.filter_by_field(self.data, filt, 'unique_code')
        return domain_prototype(self.data)

    def filter_by_field(self, source: list, filt: filter_dto, field: str) -> list:

        validator.validate_not_none(source, 'source')
        validator.validate_not_none(filt, 'filt')
        validator.validate_non_empty(field, 'field')

        if not getattr(filt, field, None):
            return source

        result = []
        for item in source:
            if self.match_field(getattr(item, field, None), getattr(filt, field), filt.type):
                result.append(item)
            elif self.filter_nested(item, filt, field):
                result.append(item)

        return result

    def filter_nested(self, item, filt: filter_dto, field: str) -> bool:
        validator.validate_not_none(item, 'item')
        validator.validate_not_none(filt, 'filt')
        validator.validate_non_empty(field, 'field')

        for attr_name in dir(item):
            attr_value = getattr(item, attr_name)
            if isinstance(attr_value, abstract_reference) and self.match_field(getattr(attr_value, field, None), getattr(filt, field), filt.type):
                return True
            elif isinstance(attr_value, list):
                for nested_item in attr_value:
                    if isinstance(nested_item, abstract_reference) and self.match_field(getattr(nested_item, field, None), getattr(filt, field), filt.type):
                        return True
        return False

    def match_field(self, field_value: str, filter_value: str, filter_type: filter_type) -> bool:

        if not field_value or not filter_value:
            return False

        try:
            return self.matcher.match_field(field_value, filter_value, filter_type)
        except argument_exception as ae:
            print(f"Ошибка аргумента: {ae}")
            return False
        except operation_exception as ce:
            print(f"Ошибка преобразования: {ce}")
            return False
        except Exception as ex:
            print(f"Ошибка: {ex}")
            return False
