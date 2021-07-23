from typing import Optional


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"{self.status_code} {self.message}"


# client error
class HTTPBadRequestException(HTTPException):
    def __init__(self, message: Optional[str] = "Bad Request"):
        super().__init__(400, message)


class HTTPUnauthorizedException(HTTPException):
    def __init__(self, message: Optional[str] = "Unauthorized"):
        super().__init__(401, message)


class HTTPForbiddenException(HTTPException):
    def __init__(self, message: Optional[str] = "Forbidden"):
        super().__init__(403, message)


class HTTPNotFoundException(HTTPException):
    def __init__(self, message: Optional[str] = "Not Found"):
        super().__init__(404, message)


class HTTPMethodNotAllowedException(HTTPException):
    def __init__(self, message: Optional[str] = "Method Not Allowed"):
        super().__init__(405, message)


# server errors
class HTTPInternalServerErrorException(HTTPException):
    def __init__(self, message: Optional[str] = "Internal Server Error"):
        super().__init__(500, message)
