from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta


def defaut_date():
    # Next 2 days if it is Saturday
    return now() + timedelta(days=1) if now().weekday() != 5 else now() + timedelta(days=2)

def alphanumeric(value: str) -> None:
    if not value.isalnum():
        raise ValidationError('Not an alphanumeric text')


def numeric(value: str) -> None:
    if not value.isnumeric():
        raise ValidationError('Not an numeric text')