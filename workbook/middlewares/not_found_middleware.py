from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status

from workbook.middlewares.exception_handler import ExceptionHandler


class ObjectDoesNotExistHandler(ExceptionHandler):
    """Handle uncaught exceptions instead of raising a 404."""

    def handle(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            return JsonResponse({'error': str(exception)}, status=status.HTTP_404_NOT_FOUND)

        return None
