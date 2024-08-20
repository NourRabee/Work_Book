import uuid
from django.utils import timezone

from workbook.models.models import Session


class SessionService:
    def get_time_difference(self, session_start_time):
        time_difference = timezone.now() - session_start_time
        return time_difference.total_seconds() / 60

    def is_valid(self, session_start_time):
        return self.get_time_difference(session_start_time) < 1

    def get(self, user_id):

        session = Session.objects.filter(user_id=user_id).order_by('-token_start_time').first()  # '-' desc

        if session and self.is_valid(session.token_start_time):
            return session

        return None

    def update(self, session):
        session.token_start_time = timezone.now()
        session.save()

    def create(self, user_id):
        return Session.objects.create(token=uuid.uuid1(), user_id=user_id)

    def get_or_create(self, user_id):
        session = self.get(user_id)

        if session is None:
            session = self.create(user_id)
        else:
            self.update(session)

        return session

    def is_valid_timeout(self, session_start_time):
        return 1 < self.get_time_difference(session_start_time) < 2
