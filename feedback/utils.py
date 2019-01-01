from uuid import UUID


def is_uuid(value):
    """
    Validate a value to be or not to be a UUID4
    """
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False
