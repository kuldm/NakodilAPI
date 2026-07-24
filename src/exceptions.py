class NakodilException(Exception):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class JobNotFoundException(NakodilException):
    status_code = 404
    detail = "Задача не найдена"


class UserNotFoundException(NakodilException):
    status_code = 404
    detail = "Пользователь не найдена"


class SeatsConflictException(NakodilException):
    status_code = 409
    detail = "Места уже забронированы"


class EventDoesNotBelongToOrganizerException(NakodilException):
    status_code = 400
    detail = "Мероприятие не принадлежит организатору"


class EventSeatsIsEmptyException(NakodilException):
    status_code = 404
    detail = "Список связанных мест и мероприятий пуст"


class BookingsIsEmptyException(NakodilException):
    status_code = 404
    detail = "Список заказов пуст"


class EventNotFoundException(NakodilException):
    status_code = 400
    detail = "Мероприятие не найдено"
