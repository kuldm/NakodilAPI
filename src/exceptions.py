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


class EventDoesNotBelongToOrganizerException(NakodilException):
    detail = "Мероприятие не принадлежит организатору"


class EventSeatsIsEmptyException(NakodilException):
    detail = "Список связанных мест и мероприятий пуст"


class BookingsIsEmptyException(NakodilException):
    detail = "Список заказов пуст"


class EventNotFoundException(NakodilException):
    detail = "Мероприятие не найдено"


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


class EventDoesNotBelongToOrganizerHTTPException(NakodilHTTPException):
    status_code = 400
    detail = "Мероприятие не принадлежит организатору"


class EventNotFoundHTTPException(NakodilHTTPException):
    status_code = 400
    detail = "Мероприятие не найдено"