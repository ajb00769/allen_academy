from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from secrets import token_hex
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r"^\+?\d{8,15}$",
    message="Phone number must follow the format '+99999999' between 8-15 digits long.",
)


def date_time_handler(format):
    match format:
        case "year":
            return datetime.now().year
        case "timestamp":
            return datetime.now()
        case "date":
            return date.today()
        case "key_expiry":
            return date.today() + relativedelta(months=1)
        case _:
            raise ValueError(
                "Invalid format provided. Expected 'year', 'timestamp', or 'date'."
            )


def generate_account_id(all_account_id_counts):
    """
    all_account_id_counts should have the logic to take the current year into account.
    Table.objects.filter(column__startswith='year').count()
    """
    if all_account_id_counts > 99999:
        return ValueError(
            {
                "error": "ID length exceeded. More than 99,999 IDs created for the year.",
            }
        )

    year = str(datetime.now().year)
    fill = str(all_account_id_counts).zfill(5)
    return year + fill


def generate_registration_key():
    token = token_hex(8)
    return "-".join(token[i : i + 4] for i in range(0, len(token), 4))


def get_age(birthday):
    """
    birthday parameter must follow the format "YYYY-MM-DD", for example "2024-12-31".
    Added if i to the list comprehension just in case a extra dashes or spaces are
    passed in as arguments.
    """
    bday_str_to_int = [int(i) for i in birthday.split("-") if i]
    bday_date_obj = date(*bday_str_to_int)
    delta = relativedelta(date.today(), bday_date_obj)
    return delta.years
