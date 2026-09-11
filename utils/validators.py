import re
from decimal import Decimal, InvalidOperation


def validate_name(name):
    name = name.strip()

    if not name:
        return False, "Name cannot be empty."

    if len(name) < 3:
        return False, "Name must contain at least 3 characters."

    if not re.fullmatch(r"[A-Za-z ]+", name):
        return False, "Name should contain only letters and spaces."

    return True, name


def validate_phone(phone):
    phone = phone.strip()

    if not re.fullmatch(r"[6-9]\d{9}", phone):
        return False, "Phone number must be a valid 10-digit Indian mobile number."

    return True, phone


def validate_email(email):
    email = email.strip()

    if not email:
        return True, None

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        return False, "Please enter a valid email address."

    return True, email


def validate_pin(pin):
    pin = pin.strip()

    if not re.fullmatch(r"\d{4}", pin):
        return False, "PIN must contain exactly 4 digits."

    return True, pin


def validate_amount(amount):
    amount = amount.strip()

    try:
        value = Decimal(amount)

        if value <= 0:
            return False, "Amount must be greater than zero."

        if value.as_tuple().exponent < -2:
            return False, "Amount can have a maximum of 2 decimal places."

        return True, value

    except InvalidOperation:
        return False, "Please enter a valid amount."