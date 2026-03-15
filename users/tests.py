from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserAuthApiTests(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "first_name": "Ivan",
                "last_name": "Petrov",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_user_can_get_jwt_token_by_email(self):
        user = User.objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="SecurePass123!",
        )

        response = self.client.post(
            reverse("token-obtain-pair"),
            {"email": user.email, "password": "SecurePass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
