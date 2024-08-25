import uuid
from datetime import datetime, timezone

from workbook.helpers import session_helper
from workbook.models.models import Session
from workbook.constants import *


class SessionService:

    def is_valid(self, session_start_time):
        return session_helper.get_time_difference(session_start_time) < SESSION_VALID_TIME

    def get(self, user_id):
        session = Session.objects.filter(user_id=user_id).order_by('-token_start_time').first()  # '-' desc

        return session if session and self.is_valid(session.token_start_time) else None

    def refresh_token_time(self, session):
        session.token_start_time = datetime.now(timezone.utc)
        session.save()

    def create(self, user_id):
        return Session.objects.create(token=uuid.uuid1().hex, user_id=user_id)

    def is_valid_timeout(self, session_start_time):
        return SESSION_VALID_TIME <= session_helper.get_time_difference(
            session_start_time) < SESSION_TIMEOUT
