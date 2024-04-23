from datetime import date


def get_current_year() -> int:
    return date.today().year


def get_year_choices() -> list[int]:
    return [year for year in range(2000, date.today().year + 2)]


def get_current_date() -> date:
    return date.today()
