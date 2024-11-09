from src.models.nomenclature_model import nomenclature_model
from src.dto.domain_prototype import domain_prototype
from src.dto.filter_dto import filter_dto
from src.dto.observe_service import observe_service
from src.core.event_type import event_type
from src.data_reposity import data_reposity
from src.dto.filter_type import filter_type
from src.core.abstract_logic import abstract_logic

class NomenclatureService(abstract_logic):
    def __init__(self, repository: data_reposity):
        observe_service.append(self)
        self.__repository = repository

    def get_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            return {"error": "Unique code is required."}

        nomenclature_filter = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        existing_nomenclatures = self.filter_model(nomenclature_filter)

        if not existing_nomenclatures:
            return {"status": "Номенклатура с указанным уникальным кодом не найдена."}

        return existing_nomenclatures

    def add_nomenclature(self, request) -> nomenclature_model:
        name = request.get('name')
        full_name = request.get('full_name')
        group_id = request.get('group_id')
        range_id = request.get('range_id')

        group = self.get_related_entity(group_id, data_reposity.group_key(), "Группа")
        if not group:
            return {"status": f"Группа с ID '{group_id}' не найдена."}

        range_ = self.get_related_entity(range_id, data_reposity.range_key(), "Диапазон")
        if not range_:
            return {"status": f"Диапазон с ID '{range_id}' не найден."}

        nomenclature = nomenclature_model.create(name, full_name, group, range_)
        if self.is_nomenclature_exists(nomenclature.unique_code):
            return {"status": f"Номенклатура с уникальным кодом '{nomenclature.unique_code}' уже существует."}

        self.__repository.data[data_reposity.nomenclature_key()].append(nomenclature)
        return nomenclature

    def update_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            return {"error": "Отсутствует уникальный код!"}

        nomenclature = self.get_nomenclature_by_code(unique_code)
        if not nomenclature:
            return {"status": f"Номенклатура с уникальным кодом '{unique_code}' не найдена."}

        self.update_nomenclature_fields(nomenclature, request)
        self.trigger_events(request)

        return {"status": "Номенклатура успешно обновлена"}

    def delete_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            return {"error": "Отсутствует уникальный код!"}

        nomenclature = self.get_nomenclature_by_code(unique_code)
        if not nomenclature:
            return {"status": f"Номенклатура с уникальным кодом '{unique_code}' не найдена."}

        if self.is_nomenclature_in_use(nomenclature):
            return {"status": f"Номенклатура '{unique_code}' не может быть удалена, так как она используется."}

        self.__repository.data[data_reposity.nomenclature_key()] = [
            n for n in self.__repository.data[data_reposity.nomenclature_key()] if n.unique_code != unique_code
        ]
        return {"status": "Номенклатура успешно удалена"}

    def filter_model(self, filt: filter_dto, key=data_reposity.nomenclature_key()) -> list[nomenclature_model]:
        models = self.__repository.data.get(key, [])
        prototype = domain_prototype(models)
        filtered_prototype = prototype.create(models, filt)
        return filtered_prototype.data

    def get_related_entity(self, unique_code, key, entity_name):
        entity_filter = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        return next(iter(self.filter_model(entity_filter, key)), None)

    def is_nomenclature_exists(self, unique_code):
        nomenclature_filter = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        return bool(self.filter_model(nomenclature_filter))

    def get_nomenclature_by_code(self, unique_code):
        nomenclature_filter = filter_dto(unique_code=unique_code, type=filter_type.EQUALS)
        return self.filter_model(nomenclature_filter)[0] if self.filter_model(nomenclature_filter) else None

    def update_nomenclature_fields(self, nomenclature, request):
        if 'name' in request:
            nomenclature.name = request['name']
        if 'full_name' in request:
            nomenclature.full_name = request['full_name']

        if 'group_id' in request:
            group = self.get_related_entity(request['group_id'], data_reposity.group_key(), "Группа")
            if not group:
                return {"status": f"Группа с ID '{request['group_id']}' не найдена."}
            nomenclature.group = group

        if 'range_id' in request:
            range_ = self.get_related_entity(request['range_id'], data_reposity.range_key(), "Диапазон")
            if not range_:
                return {"status": f"Диапазон с ID '{request['range_id']}' не найден."}
            nomenclature.range = range_

    def trigger_events(self, request):
        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE_FROM_RECIPE, request)
        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE_FROM_TRANSACTION, request)

    def is_nomenclature_in_use(self, nomenclature):
        return self.is_nomenclature_in_recipes(nomenclature) or self.is_nomenclature_in_saved_data(nomenclature)

    def is_nomenclature_in_recipes(self, nomenclature: nomenclature_model) -> bool:
        return self.is_nomenclature_in_data(nomenclature, data_reposity.recipes_key())

    def is_nomenclature_in_saved_data(self, nomenclature: nomenclature_model) -> bool:
        return self.is_nomenclature_in_data(nomenclature, data_reposity.transactions_key())

    def is_nomenclature_in_data(self, nomenclature: nomenclature_model, key) -> bool:
        nomenclature_filter = filter_dto(unique_code=nomenclature.unique_code, type=filter_type.EQUALS)
        filtered_data = self.filter_model(nomenclature_filter, key)
        return bool(filtered_data)

    def set_exception(self, ex: Exception):
        super().set_exception(ex)

    def handle_event(self, event_type: event_type, params):
        super().handle_event(event_type, params)

        if event_type == event_type.CHANGE_NOMENCLATURE:
            return self.update_nomenclature(params)
        elif event_type == event_type.DELETE_NOMENCLATURE:
            return self.delete_nomenclature(params)
        return {"status": "fail"}

