from django.core.exceptions import BadRequest
from django.http import JsonResponse


class BadRequestHandler:
    """Handle uncaught exceptions instead of raising a 400."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, BadRequest):
            return JsonResponse({'error': str(exception)}, status=400)

        return None
