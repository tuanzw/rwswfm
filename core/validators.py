from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta

from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and hyphens are allowed.')

def defaut_date():
    # Next 2 days if it is Saturday
    return now() + timedelta(days=1) if now().weekday() != 5 else now() + timedelta(days=2)