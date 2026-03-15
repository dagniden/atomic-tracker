def validate_habit_business_rules(*, is_pleasant, reward, related_habit, duration, periodicity):
    errors = {}

    if reward and related_habit:
        errors["non_field_errors"] = ["Нельзя одновременно указывать вознаграждение и связанную привычку."]

    if duration is not None and duration > 120:
        errors["duration"] = ["Время выполнения привычки не должно превышать 120 секунд."]

    if periodicity is not None and not 1 <= periodicity <= 7:
        errors["periodicity"] = ["Периодичность должна быть от 1 до 7 дней."]

    if is_pleasant and reward:
        errors["reward"] = ["Приятная привычка не может иметь вознаграждение."]

    if is_pleasant and related_habit:
        errors["related_habit"] = ["Приятная привычка не может ссылаться на другую привычку."]

    if related_habit and not related_habit.is_pleasant:
        errors["related_habit"] = ["Связанная привычка должна быть приятной."]

    return errors
