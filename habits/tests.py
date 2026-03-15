from datetime import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit


User = get_user_model()


class HabitApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner@example.com",
            email="owner@example.com",
            password="SecurePass123!",
        )
        self.other_user = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="SecurePass123!",
        )
        self.client.force_authenticate(self.user)

    def test_user_can_create_habit(self):
        response = self.client.post(
            reverse("habit-list"),
            {
                "action": "Read 20 pages",
                "place": "Home",
                "time": "21:00",
                "periodicity": 1,
                "duration": 30,
                "is_pleasant": False,
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.get().user, self.user)

    def test_validator_rejects_reward_and_related_habit_together(self):
        pleasant = Habit.objects.create(
            user=self.user,
            action="Hot bath",
            place="Bathroom",
            time=time(22, 0),
            is_pleasant=True,
            periodicity=1,
            duration=20,
        )

        response = self.client.post(
            reverse("habit-list"),
            {
                "action": "Run",
                "place": "Park",
                "time": "07:00",
                "periodicity": 1,
                "duration": 30,
                "is_pleasant": False,
                "reward": "Coffee",
                "related_habit": pleasant.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_rejects_non_pleasant_related_habit(self):
        related = Habit.objects.create(
            user=self.user,
            action="Run",
            place="Park",
            time=time(7, 0),
            is_pleasant=False,
            periodicity=1,
            duration=30,
        )

        response = self.client.post(
            reverse("habit-list"),
            {
                "action": "Read",
                "place": "Home",
                "time": "08:00",
                "periodicity": 1,
                "duration": 30,
                "is_pleasant": False,
                "related_habit": related.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("related_habit", response.data)

    def test_owner_only_sees_own_habits(self):
        Habit.objects.create(
            user=self.user,
            action="Read",
            place="Home",
            time=time(21, 0),
            is_pleasant=False,
            periodicity=1,
            duration=30,
        )
        Habit.objects.create(
            user=self.other_user,
            action="Run",
            place="Park",
            time=time(7, 0),
            is_pleasant=False,
            periodicity=1,
            duration=30,
        )

        response = self.client.get(reverse("habit-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_owner_cannot_access_other_users_habit(self):
        habit = Habit.objects.create(
            user=self.other_user,
            action="Run",
            place="Park",
            time=time(7, 0),
            is_pleasant=False,
            periodicity=1,
            duration=30,
        )

        response = self.client.get(reverse("habit-detail", args=[habit.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_endpoint_returns_public_habits(self):
        Habit.objects.create(
            user=self.other_user,
            action="Public habit",
            place="Park",
            time=time(7, 0),
            is_pleasant=False,
            periodicity=1,
            duration=30,
            is_public=True,
        )
        Habit.objects.create(
            user=self.other_user,
            action="Private habit",
            place="Home",
            time=time(21, 0),
            is_pleasant=False,
            periodicity=1,
            duration=30,
            is_public=False,
        )

        response = self.client.get(reverse("public-habit-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
