from datetime import date, time
from django.core.exceptions import ValidationError


def format_subject_block(subject_code: str, subject_block: str) -> str:
    return f"{subject_code}-{subject_block}"


def class_end_date_validator(start_date: str, end_date: str):
    start_date_input = date(*[int(item) for item in (start_date.split("-"))])
    end_date_input = date(*[int(item) for item in (end_date.split("-"))])

    if start_date_input > end_date_input:
        raise ValidationError(
            "Class end date cannot take place before class start date."
        )


def class_end_time_validator(start_time: time, end_time: time):
    start_time_input = time(*[int(item) for item in (start_time.split(":"))])
    end_time_input = time(*[int(item) for item in (end_time.split(":"))])

    if start_time_input > end_time_input:
        raise ValidationError(
            "Class end time cannot take place before class start time."
        )
