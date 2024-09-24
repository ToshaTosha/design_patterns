from src.models.abstract_reference import abstract_reference

class nomenclature_group_model(abstract_reference):
    def __init__(self):
        super().__init__()

    """
        Default группа - сырье (фабричный метод)
        """

    @staticmethod
    def default_group_source():
        item = nomenclature_group_model()
        item.name = "Сырье"
        return item

    """
    Default группа - замарозка (фабричный метод)
    """

    @staticmethod
    def default_group_cold():
        item = nomenclature_group_model()
        item.name = "Заморозка"
        return item

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)