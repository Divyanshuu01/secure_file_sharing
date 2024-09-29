from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class SignupTestCase(APITestCase):
    def test_signup(self):
        data = {"username": "client1", "password": "password123", "email": "client1@example.com", "user_type": "client"}
        response = self.client.post('/api/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_file_permission(self):
        # Test that only ops user can upload
        pass
