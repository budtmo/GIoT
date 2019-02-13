import json

from src.views.tests import BaseTest


class TestUpdateDeviceInformation(BaseTest):
    """Tests to update device information."""

    def setUp(self):
        super().setUp()
        self.headers = {'Content-Type': 'application/json'}
        self.url = '/device/{id}'.format(id=1)
        self.payload = {'name': 'device10'}

    def test_update_employee(self):
        self.insert_employee()
        res = self.test_app.put(self.url, headers=self.headers, data=json.dumps(self.payload))
        self.assertEqual(res.status_code, 201)
