from django.core.exceptions import BadRequest, ObjectDoesNotExist
from rest_framework.exceptions import NotAuthenticated

from workbook.middlewares.bad_request_middleware import BadRequestHandler
from workbook.middlewares.not_authenticated import NotAuthenticatedHandler
from workbook.middlewares.not_found_middleware import ObjectDoesNotExistHandler


class ExceptionHandlerFactory:
    def __init__(self):
        self.handler_map = {
            BadRequest: BadRequestHandler(),
            ObjectDoesNotExist: ObjectDoesNotExistHandler(),
            NotAuthenticated: NotAuthenticatedHandler(),
        }

    def get_exception_handler(self, exception):
        for exc_type, handler in self.handler_map.items():
            if isinstance(exception, exc_type):
                return handler

        return None
