class PaulException(Exception):
    pass


class InvalidEventException(PaulException, ValueError):
    pass
