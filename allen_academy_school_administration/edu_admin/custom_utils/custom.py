from datetime import date, time
from django.core.exceptions import ValidationError


def format_subject_block(subject_code: str, subject_block: str) -> str:
    return f"{subject_code}-{subject_block}"


def class_end_date_validator(start_date: date, end_date: date):
    if start_date > end_date:
        raise ValidationError(
            "Class end date cannot take place before class start date."
        )


def class_end_time_validator(start_time: time, end_time: time):
    if start_time > end_time:
        raise ValidationError(
            "Class end time cannot take place before class start time."
        )
