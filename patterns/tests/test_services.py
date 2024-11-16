import unittest
from flask import Flask, jsonify, request

from main import nomenclature_service_instance, manager
from src.dto.observe_service import observe_service
from src.models.nomenclature_model import nomenclature_model
from src.reports.report_factory import report_factory
from main import app


class NomenclatureAPITests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_nomenclature_success(self):
        nomenclature_service_instance.get_nomenclature = lambda args: [{"id": 1, "name": "Test Item"}]
        report_factory(manager).create = lambda format: report_factory(manager)
        report_factory(manager).create().result = [{"id": 1, "name": "Test Item"}]

        response = self.app.get('/api/nomenclature')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": 1, "name": "Test Item"}])

    def test_get_nomenclature_error(self):
        nomenclature_service_instance.get_nomenclature = lambda args: {"error": "Not found"}

        response = self.app.get('/api/nomenclature')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Not found"})

    def test_add_nomenclature_success(self):
        nomenclature_service_instance.add_nomenclature = lambda json: nomenclature_model(id=1, name="New Item")
        report_factory(manager).create = lambda format: report_factory(manager)
        report_factory(manager).create().result = [{"id": 1, "name": "New Item"}]

        response = self.app.put('/api/nomenclature', json={"name": "New Item"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, [{"id": 1, "name": "New Item"}])

    def test_add_nomenclature_failure(self):
        nomenclature_service_instance.add_nomenclature = lambda json: {"error": "Invalid data"}

        response = self.app.put('/api/nomenclature', json={"name": "Invalid Item"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid data"})

    def test_update_nomenclature(self):
        observe_service.raise_event = lambda event_type, json: {type(nomenclature_service_instance).__name__: "Updated"}

        response = self.app.patch('/api/nomenclature', json={"id": 1, "name": "Updated Item"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Updated")

    def test_delete_nomenclature_success(self):
        observe_service.raise_event = lambda event_type, json: {type(nomenclature_service_instance).__name__: "Deleted"}

        response = self.app.delete('/api/nomenclature', json={"id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Deleted")

    def test_delete_nomenclature_failure(self):
        observe_service.raise_event = lambda event_type, json: (_ for _ in ()).throw(ValueError("Deletion failed"))

        response = self.app.delete('/api/nomenclature', json={"id": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Deletion failed"})



if __name__ == '__main__':
    unittest.main()
