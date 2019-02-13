from src.views.tests import BaseTest


class TestDeleteDevice(BaseTest):
    """Tests to delete device from the list."""

    def test_delete_device(self):
        self.register_device()
        res = self.test_app.delete('/device/{id}'.format(id=1))
        self.assertEqual(res.status_code, 204)

    def test_delete_non_existing_device(self):
        res = self.test_app.delete('/device/{id}'.format(id=5))
        self.assertEqual(res.status_code, 404)
