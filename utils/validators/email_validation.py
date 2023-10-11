from django.core.exceptions import ValidationError
import re

EMAIL_REGEX = "^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"


def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        raise ValidationError("invalid email")
