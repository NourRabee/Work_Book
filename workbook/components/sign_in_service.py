from workbook.components.password_service import PasswordService
from workbook.components.session_service import SessionService
from workbook.models.models import User, Session


class SignInService:
    def __init__(self):
        self.password_service = PasswordService()
        self.session_service = SessionService()

    def authenticate_user(self, email, password):

        user = User.objects.get(email=email)

        authenticated = self.password_service.validate(password, user.salt, user.password)

        if authenticated:
            session = self.session_service.create(user.id)
            return session.token

        return None

    def authenticate_session(self, session_id):

        session = Session.objects.get(token=session_id)

        is_valid_session = self.session_service.is_valid(session.token_start_time)

        if is_valid_session:
            self.session_service.refresh_token_time(session)
            return session.token

        else:
            is_valid_timeout = self.session_service.is_valid_timeout(session.token_start_time)
            if is_valid_timeout:
                session = self.session_service.create(session.user_id)
                return session.token
        return None
