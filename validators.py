from datetime import datetime
import re


def validate_name(name):
    return name.replace(" ", "").isalpha()


def validate_gender(gender):
    return gender.lower() in ["male", "female", "other"]


def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10


def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_positive_number(value):
    try:
        return float(value) > 0
    except ValueError:
        return False


def validate_required(value):
    return bool(value.strip())


def validate_time_slot(time_slot):
    pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9]-(0[1-9]|1[0-2]):[0-5][0-9]$"
    return re.match(pattern, time_slot) is not None