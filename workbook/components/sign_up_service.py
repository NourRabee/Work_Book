from workbook.components.password_service import PasswordService
from workbook.enums import UserType
from workbook.models.models import User, Customer, Worker
from workbook.serializers.sign_up_serializer import SignUpResponseSerializer


class SignUpService:
    def __init__(self):
        self.password_service = PasswordService()

    def create(self, user_serializer):
        validated_data = user_serializer.validated_data

        salt = self.password_service.generate_salt()
        validated_data['salt'] = salt
        validated_data['password'] = self.password_service.hash_with_salt(validated_data['password'], salt)
        user = User.objects.create(**validated_data)

        if validated_data['role'] == UserType.CUSTOMER.value:
            customer = Customer(user=user)
            customer.save()
        else:
            worker = Worker(user=user)
            worker.save()

        return SignUpResponseSerializer(user).data

    def email_existence_check(self, email):
        return bool(User.objects.filter(email=email).first())