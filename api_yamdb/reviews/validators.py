from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_date(value):
    if value > timezone.now().year:
        raise ValidationError("Выбрана дата в будущем")
    elif value < 0:
        raise ValidationError("Нельзя указать отрицательное значение")


def validate_lenght(value):
    if len(value) > 256:
        raise ValidationError("Длина описания не должна превышать 256 симолов")
