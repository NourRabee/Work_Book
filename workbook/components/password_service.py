import hashlib
from django.utils.crypto import get_random_string


class PasswordService:

    def generate_salt(self, length=12):
        return get_random_string(length)

    def hash_with_salt(self, plain_password, salt):
        combined = plain_password + salt
        hashed_password = hashlib.sha256(combined.encode('utf-8')).hexdigest()

        return hashed_password

    def validate(self, plain_password, salt, hashed_password):
        combined = plain_password + salt

        validated = hashlib.sha256(combined.encode('utf-8')).hexdigest()

        return hashed_password == validated
