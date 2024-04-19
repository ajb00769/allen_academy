from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


phone_validator = RegexValidator(
    regex=r"^\+?\d{8,15}$",
    message="Phone number must follow the format '+99999999' between 8-15 digits long.",
)


def get_age(birthday: datetime) -> int:
    # accepts datetime.date object
    delta = relativedelta(date.today(), birthday)
    return delta.years


def student_age_validator(birthday):
    min_age = 11
    user_age = get_age(birthday)
    if user_age < min_age:
        raise ValidationError(f"User too young. Must be at least {min_age} years old.")


def staff_parent_age_validator(birthday):
    min_age = 21
    user_age = get_age(birthday)
    if user_age < min_age:
        raise ValidationError(f"User too young. Must be at least {min_age} years old.")
