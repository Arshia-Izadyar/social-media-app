import re
from django.core.exceptions import ValidationError

PHONE_NUMBER_REGEX = "^09(1[0-9]|2[0-2]|3[0-9]|9[0-9])[0-9]{7}$"


def validate_phone_number(number):
    if not re.match(PHONE_NUMBER_REGEX, number):
        raise ValidationError("invalid phone number")


