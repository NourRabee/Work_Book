from django.http import JsonResponse
from rest_framework.exceptions import NotAuthenticated

from workbook.middlewares.exception_handler import ExceptionHandler


class NotAuthenticatedHandler(ExceptionHandler):
    """Handle uncaught exceptions instead of raising a 401."""

    def handle(self, request, exception):
        if isinstance(exception, NotAuthenticated):
            return JsonResponse({'error': str(exception)}, status=400)

        return None
