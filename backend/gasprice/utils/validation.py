"""Validation utils
"""
from typing import Any, Iterable


class ValidationError(Exception):
    pass


def validate_input(
        raw_value: Any,
        expected_type: type,
        var_name: str = None,
        message: str = None,
        min_value=None,
        max_value=None,
        choices: Iterable = None
) -> Any:
    """Validate input, raise ValidationError if invalid

    Args:
        raw_value: user input data
        expected_type: type to try convert into
        var_name: variable name for automatic message, ignore if have message
        message: custom error message
        min_value: minimum value, only for numeric type
        max_value: maximum value, only for numeric type
        choices: value must be in this list

    Returns:
        return expected converted value

    Raise ValidationError if invalid

    """
    try:
        if isinstance(raw_value, expected_type):
            value = raw_value
        elif isinstance(raw_value, str):
            value = expected_type(raw_value.strip())
        else:
            value = expected_type(raw_value)
    except (TypeError, ValueError, AttributeError):
        if message:
            raise ValidationError(message)
        raise ValidationError(
            f'Invalid `{var_name}`, expected {expected_type.__name__}')

    errors = []

    if isinstance(value, (int, float, complex)):
        if min_value is not None and min_value > value:
            errors.append(f'must larger or equal {min_value}')
        if max_value is not None and max_value < value:
            errors.append(f'must smaller or equal {max_value}')

    if choices is not None and value not in choices:
        errors.append(f'only {choices} allowed')

    if errors:
        if message:
            raise ValidationError(message)
        message = ', '.join(errors)
        raise ValidationError(f'Invalid `{var_name}`, {message}')

    return value
