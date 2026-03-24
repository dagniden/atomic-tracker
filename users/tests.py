from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthAPITests(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "ivan",
                "email": "ivan@example.com",
                "password": "SecurePass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="ivan@example.com").exists())
        self.assertNotIn("password", response.data)

    def test_user_can_login_with_email_and_password(self):
        User.objects.create_user(
            username="ivan",
            email="ivan@example.com",
            password="SecurePass123!",
        )

        response = self.client.post(
            reverse("users:login"),
            {
                "email": "ivan@example.com",
                "password": "SecurePass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_authenticated_user_cannot_access_registration_only_endpoint_methods(self):
        response = self.client.get(reverse("users:register"))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
