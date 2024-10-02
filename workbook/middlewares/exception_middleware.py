from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from workbook.middlewares.exception_handler_factory import ExceptionHandlerFactory


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exception_handler_factory = ExceptionHandlerFactory()

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        handler = self.exception_handler_factory.get_exception_handler(exception)

        if handler:
            response = handler.handle(request, exception)
            if response:
                return response

        return JsonResponse(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
