from fastapi import HTTPException


class NakodilException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class JobNotFoundException(NakodilException):
    detail = "Задача не найдена"


class UserNotFoundException(NakodilException):
    detail = "Пользователь не найдена"


class SeatsConflictException(NakodilException):
    detail = "Места уже забронированы"


class NakodilHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class JobNotFoundHTTPException(NakodilHTTPException):
    status_code = 404
    detail = "Задача не найдена"


class UserNotFoundHTTPException(NakodilHTTPException):
    status_code = 404
    detail = "Пользователь не найдена"


class SeatsConflictHTTPException(NakodilHTTPException):
    status_code = 409
    detail = "Места уже забронированы"
