from src.views.tests import BaseTest


class TestHealthCheck(BaseTest):
    """Tests for health-check endpoint."""

    def test_health_check(self):
        response = self.test_app.get('/')
        self.assertEqual(response.status_code, 200)
