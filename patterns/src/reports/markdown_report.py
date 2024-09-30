from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception

class markdown_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.MARKDOWN

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        first_model = data[0]

        # Список полей от типа назначения
        fields = self.get_class_fields(first_model)

        self.result = "|"
        divider = "|"
        for field in fields:
            self.result += f"{str(field)}|"
            divider += "-" * (len(field)) + "|"

        self.result += "\n"
        self.result += divider + "\n"

        for row in data:
            self.result += "|"
            for field in fields:
                value = getattr(row, field)
                self.result += f"{value}|"
            self.result += "\n"
