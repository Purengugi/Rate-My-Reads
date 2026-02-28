import pytest
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from .models import User
from .serializers import UserSerializer
from .views import sign_up


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@example.com", name="Test User", password="testexamplepass")

    def test_create_user_not_allowed(self):
        url = reverse('user-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming only one user exists


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_sign_up_success(self):
        request = self.factory.post('/sign_up/', {'email': 'test@example.com', 'password': 'test123'})
        response = sign_up(request)
        self.assertEqual(response.status_code, 201)  # Created

    def test_sign_up_invalid_data(self):
        request = self.factory.post('/sign_up/', {'email': 'invalid_email', 'password': 'test123'})
        response = sign_up(request)
        self.assertEqual(response.status_code, 400)  # Bad Request


class UserListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@example.com", name="Test User")

    def test_list_users(self):
        url = reverse('user-list-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)