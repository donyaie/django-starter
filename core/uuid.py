import shortuuid


def create_short_uuid():
    """
    Creates an suid.

    :return: string: The generated suid.

    """
    return shortuuid.uuid()
