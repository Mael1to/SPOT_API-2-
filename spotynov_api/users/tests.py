from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_login(self):
        response = self.client.post("/login/", {"username": "testuser", "password": "12345"})
        self.assertEqual(response.status_code, 200)
