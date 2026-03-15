from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_habit_business_rules


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "action",
            "place",
            "time",
            "is_pleasant",
            "related_habit",
            "reward",
            "periodicity",
            "duration",
            "is_public",
            "last_reminded_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "last_reminded_at", "created_at", "updated_at")

    def validate_related_habit(self, value):
        request = self.context.get("request")
        if value and request and value.user != request.user:
            raise serializers.ValidationError("Можно использовать только свои привычки как связанные.")
        return value

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        is_pleasant = attrs.get("is_pleasant", getattr(instance, "is_pleasant", False))
        reward = attrs.get("reward", getattr(instance, "reward", ""))
        related_habit = attrs.get("related_habit", getattr(instance, "related_habit", None))
        duration = attrs.get("duration", getattr(instance, "duration", None))
        periodicity = attrs.get("periodicity", getattr(instance, "periodicity", 1))

        errors = validate_habit_business_rules(
            is_pleasant=is_pleasant,
            reward=reward,
            related_habit=related_habit,
            duration=duration,
            periodicity=periodicity,
        )
        if errors:
            raise serializers.ValidationError(errors)

        return attrs
