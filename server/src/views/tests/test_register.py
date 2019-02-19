import json

from src.models.device import Device

from src.msg import warning
from src.views.tests import BaseTest


class TestRegisterDevice(BaseTest):
    """Tests to register device to the Grid."""

    def setUp(self):
        super().setUp()
        self.headers = {'Content-Type': 'application/json'}
        self.payload = {'name': 'device1', 'category': Device.Category.SIMULATOR,
                        'type': 'camera', 'version': '0.1', 'ip': 'x.x.x.x', 'port': '7100',
                        'status': Device.Status.INACTIVE}

    def test_register_device(self):
        res = self.test_app.post('/device', headers=self.headers, data=json.dumps(self.payload))
        self.assertEqual(res.status_code, 200)

        res = self.test_app.post('/device', headers=self.headers, data=json.dumps(self.payload))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.get_response_msg(res), warning.ALREADY_EXISTS)
