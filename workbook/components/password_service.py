import hashlib
from django.utils.crypto import get_random_string
from workbook.constants import *


class PasswordService:

    def generate_salt(self, length=SALT_LENGTH):
        return get_random_string(length)

    def hash_with_salt(self, plain_password, salt):
        combined = plain_password + salt
        hashed_password = hashlib.sha256(combined.encode('utf-8')).hexdigest()

        return hashed_password

    def validate(self, plain_password, salt, hashed_password):
        return hashed_password == self.hash_with_salt(plain_password, salt)
