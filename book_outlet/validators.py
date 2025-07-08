

def validate_only_big_chars(value):
    if not value.isupper():
        raise ValueError("Value must be in uppercase")