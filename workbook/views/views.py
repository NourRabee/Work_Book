import json

from django.core.exceptions import BadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workbook.components.customer_service import CustomerService
from workbook.components.sign_in_service import SignInService
from workbook.components.sign_up_service import SignUpService
from workbook.components.worker_service import WorkerService
from workbook.search_query_params import SearchQueryParameters
from workbook.serializers.customer_serializer import CustomerSerializer
from workbook.serializers.sign_up_serializer import SignUpSerializer
from workbook.serializers.worker_serializer import WorkerSerializer


class SignInView(APIView):
    def __init__(self):
        self.sign_in_service = SignInService()

    def post(self, request):
        session_id = request.GET.get('sid')

        if not session_id:
            email = request.data.get('email')
            password = request.data.get('password')
            result = self.sign_in_service.authenticate_user(email, password)
        else:
            result = self.sign_in_service.authenticate_session(session_id)

        if result:
            return Response({"token": result})
        else:
            return Response({"message": "Sign in again"}, status=401)  # Return a 401 status if authentication fails


class SignUpView(APIView):
    def __init__(self):
        self.sign_up_service = SignUpService()

    def post(self, request):
        data = json.loads(request.body)

        email_validation_result = self.sign_up_service.email_existence_check(data['email'])

        if email_validation_result:
            raise BadRequest(email_validation_result)

        user_serializer = SignUpSerializer(data=data)

        user_serializer.is_valid_raise()

        created_user = self.sign_up_service.create(user_serializer)

        return Response(created_user, status=status.HTTP_201_CREATED)


class Customer(APIView):
    def __init__(self):
        self.customer_service = CustomerService()

    def put(self, request, customer_id):
        data = request.data

        customer_serializer = CustomerSerializer(data=data)

        customer_serializer.is_valid_raise()

        updated_customer = self.customer_service.update(customer_serializer, customer_id)

        return Response(updated_customer, status=status.HTTP_201_CREATED)

    def get(self, request, customer_id):
        worker = self.customer_service.get(customer_id)
        return Response(worker, status=status.HTTP_200_OK)

    def delete(self, request, customer_id):
        result = self.customer_service.delete(customer_id)
        return Response(result, status=status.HTTP_204_NO_CONTENT)


class Worker(APIView):
    def __init__(self):
        self.worker_service = WorkerService()

    def put(self, request, worker_id):
        data = request.data
        worker_serializer = WorkerSerializer(data=data)

        worker_serializer.is_valid_raise()

        updated_worker = self.worker_service.update(worker_serializer, worker_id)

        return Response(updated_worker, status=status.HTTP_200_OK)

    def get(self, request, worker_id):
        worker = self.worker_service.get(worker_id)
        return Response(worker, status=status.HTTP_200_OK)

    def delete(self, request, worker_id):
        result = self.worker_service.delete(worker_id)
        return Response(result, status=status.HTTP_204_NO_CONTENT)


class WorkerSkills(APIView):
    def __init__(self):
        self.worker_service = WorkerService()

    def get(self, request, worker_id):
        return self.worker_service.get_skills(worker_id)


class SearchWorkers(APIView):
    def __init__(self):
        self.worker_service = WorkerService()

    def get(self, request):
        params = SearchQueryParameters(request.query_params)
        params.validate_mandatory_params()
        params.validate_params()

        result = self.worker_service.search(params)

        return Response(result, status=status.HTTP_200_OK)
