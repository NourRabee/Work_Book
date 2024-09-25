from django.http import JsonResponse
from rest_framework.exceptions import NotAuthenticated


class NotAuthenticatedHandler:
    """Handle uncaught exceptions instead of raising a 400."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, NotAuthenticated):
            return JsonResponse({'error': str(exception)}, status=400)

        return None
