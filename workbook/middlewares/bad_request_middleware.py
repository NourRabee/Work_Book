from django.core.exceptions import BadRequest
from django.http import JsonResponse

from workbook.middlewares.exception_handler import ExceptionHandler


class BadRequestHandler(ExceptionHandler):
    """Handle uncaught exceptions instead of raising a 400."""

    def handle(self, request, exception):
        if isinstance(exception, BadRequest):
            return JsonResponse({'error': str(exception)}, status=400)

        return None
