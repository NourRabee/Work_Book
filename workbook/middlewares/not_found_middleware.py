from django.http import JsonResponse
from django.contrib import messages

from workbook.middlewares.exception_handler import ExceptionHandler


class ObjectDoesNotExistHandler(ExceptionHandler):
    """Handle uncaught exceptions instead of raising a 404."""

    def handle(self, request, exception):
        table_name = str(exception.args[0]).split()[0]

        error_message = f"{table_name.capitalize()} not found."

        messages.warning(request, error_message)

        return JsonResponse({'error': error_message}, status=404)
