from src.msg import warning
from src.views.tests import BaseTest


class TestGetAllDevices(BaseTest):
    """Tests to get all devices."""

    def setUp(self):
        super().setUp()
        self.url = '/devices?page_number={0}&page_size={1}'
        self.url_filter = '/devices?page_number={0}&page_size={1}&category={2}&type={3}&status={4}'

    def test_get_devices(self):
        res = self.test_app.get(self.url.format(1, 2))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(self.get_response_msg(res), warning.NO_DATA)

        self.register_device()
        res = self.test_app.get(self.url.format(1, 2))
        self.assertEqual(res.status_code, 200)

    def test_no_page(self):
        res = self.test_app.get(self.url.format(0, 2))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(self.get_response_msg(res), warning.NO_PAGE_INFO)

    def test_invalid_page(self):
        self.register_device()
        res = self.test_app.get(self.url.format(5, 2))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(self.get_response_msg(res), warning.INVALID_PAGE)

    def test_get_devices_with_filter(self):
        self.register_device()
        res = self.test_app.get(self.url.format(1, 2, 'simulator', 'camera', 'available'))
        self.assertEqual(res.status_code, 200)


class TestGetDevice(BaseTest):
    """Tests to get a specific device."""

    def setUp(self):
        super().setUp()
        self.url = '/device?category={0}&type={1}'

    def test_get_device(self):
        self.register_device()
        res = self.test_app.get('/device/{id}'.format(id=1))
        self.assertEqual(res.status_code, 200)

    def test_get_available_device(self):
        self.register_device()
        res = self.test_app.get(self.url.format('simulator', 'camera'))
        self.assertEqual(res.status_code, 200)

        res = self.test_app.get(self.url.format('simulator', 'new-type'))
        self.assertEqual(res.status_code, 404)
