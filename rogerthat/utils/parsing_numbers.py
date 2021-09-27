from decimal import Decimal as Dec


def decimal_or_none(num_string):
    return Dec(str(num_string)) if num_string and str(num_string).replace('.', '').isdigit() else None


def decimal_or_zero(num_string):
    return Dec(str(num_string)) if num_string and str(num_string).replace('.', '').isdigit() else Dec("0")


def int_or_none(num_string):
    return int(str(num_string)) if num_string and str(num_string).isdigit() else None
