from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("id", "user", "last_reminded_at", "created_at", "updated_at")

    def validate(self, attrs):
        reward = attrs.get("reward", getattr(self.instance, "reward", None))
        related_habit = attrs.get("related_habit", getattr(self.instance, "related_habit", None))
        is_pleasant = attrs.get("is_pleasant", getattr(self.instance, "is_pleasant", False))

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        if is_pleasant and reward:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь текстовое вознаграждение."
            )

        if is_pleasant and related_habit:
            raise serializers.ValidationError(
                "Приятная привычка не может ссылаться на другую привычку."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        if self.instance and related_habit and related_habit.pk == self.instance.pk:
            raise serializers.ValidationError(
                "Нельзя связать привычку саму с собой."
            )

        return attrs
