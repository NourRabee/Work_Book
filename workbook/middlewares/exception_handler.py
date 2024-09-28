class ExceptionHandler:
    def handle(self, request, exception):
        """Handle the exception"""
        raise NotImplementedError("This method must be overridden in the subclass")
