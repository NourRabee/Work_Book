import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from workbook.components.customer_service import CustomerService
from workbook.components.image_service import ImageService
from workbook.components.reservation_service import ReservationService
from workbook.components.review_service import ReviewService
from workbook.components.search_service import SearchService
from workbook.components.sign_in_service import SignInService
from workbook.components.sign_up_service import SignUpService
from workbook.components.worker_service import WorkerService
from workbook.search_query_params import SearchQueryParameters
from workbook.serializers.customer_serializer import *
from workbook.serializers.reservation_serializer import *
from workbook.serializers.review_serializer import GetCustomerReviewSerializer, GetWorkerReviewsSerializer
from workbook.serializers.sign_up_serializer import SignUpSerializer
from workbook.serializers.worker_serializer import WorkerSerializer, SkillSerializer, WorkerDetailsSerializer


class SignInView(APIView):
    def __init__(self):
        self.sign_in_service = SignInService()

    def post(self, request):
        session_id = request.GET.get('sid')

        if not session_id:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                raise BadRequest('Both email and password are required')

            token = self.sign_in_service.authenticate_user(email, password)

            if token is None:
                raise NotAuthenticated('Sign in failed. Email or password may be incorrect.')

        else:
            token = self.sign_in_service.authenticate_session(session_id)
            if token is None:
                raise NotAuthenticated('Session expired or invalid. Please sign in again.')

        return Response({"token": token})


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
        self.image_service = ImageService()

    def put(self, request, customer_id):
        data = request.data

        image_file = request.FILES['profile_picture']
        validated_image_file = self.image_service.image_field_validation(image_file)
        data['profile_picture'] = self.image_service.image_file_to_binary(validated_image_file)

        customer_serializer = CustomerSerializer(data=data)
        customer_serializer.is_valid_raise()
        updated_customer = self.customer_service.update(customer_serializer, customer_id)

        return Response(updated_customer, status=status.HTTP_201_CREATED)

    def get(self, request, customer_id):
        customer = self.customer_service.get(customer_id)
        customer_serializer = CustomerDetailsSerializer(customer)

        return Response(customer_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, customer_id):
        result = self.customer_service.delete(customer_id)
        if result:
            return Response({"message": "Customer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return BadRequest("Failed to delete customer.")


class CustomerProfilePicture(APIView):
    def __init__(self):
        self.customer_service = CustomerService()

    def get(self, request, customer_id):
        image_format, image = self.customer_service.get_profile_picture(customer_id)

        return HttpResponse(image, content_type=f'image/{image_format}')


class Worker(APIView):
    def __init__(self):
        self.worker_service = WorkerService()
        self.image_service = ImageService()

    def put(self, request, worker_id):
        data = request.data

        image_file = request.FILES['profile_picture']
        validated_image_file = self.image_service.image_field_validation(image_file)
        data['profile_picture'] = self.image_service.image_file_to_binary(validated_image_file)

        worker_serializer = WorkerSerializer(data=data)

        worker_serializer.is_valid_raise()

        updated_worker = self.worker_service.update(worker_serializer, worker_id)

        return Response(updated_worker, status=status.HTTP_200_OK)

    def get(self, request, worker_id):
        worker = self.worker_service.get(worker_id)
        worker_serializer = WorkerDetailsSerializer(worker)

        return Response(worker_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, worker_id):
        result = self.worker_service.delete(worker_id)
        if result:
            return Response({"message": "Worker deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return BadRequest("Failed to delete worker.")


class WorkerProfilePicture(APIView):
    def __init__(self):
        self.worker_service = WorkerService()

    def get(self, request, worker_id):
        image_format, image = self.worker_service.get_profile_picture(worker_id)

        return HttpResponse(image, content_type=f'image/{image_format}')


class WorkerSkills(APIView):
    def __init__(self):
        self.worker_service = WorkerService()

    def get(self, request, worker_id):
        worker_skills = self.worker_service.get_skills(worker_id)

        serializer = SkillSerializer(worker_skills, many=True)

        return Response(serializer.data)


class SearchWorkers(APIView):
    def __init__(self):
        self.search_service = SearchService()

    def get(self, request):
        params = SearchQueryParameters(request.query_params)
        params.validate_mandatory_params()
        params.validate_params()

        result = self.search_service.search(params)

        return Response(result, status=status.HTTP_200_OK)


class CustomerReservations(APIView):
    def __init__(self):
        self.reservation_service = ReservationService()

    def get(self, request, customer_id):
        reservations = self.reservation_service.get_customer_reservations(customer_id)
        reservations_serializer = CustomerReservationResponseSerializer(reservations, many=True)

        return Response(reservations_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, customer_id):
        data = request.data
        serializer = CreateReservationSerializer(data=data)
        serializer.is_valid_raise()
        reservation_ids = self.reservation_service.create(customer_id, serializer)

        if reservation_ids:
            return Response(reservation_ids, status=status.HTTP_200_OK)
        else:
            raise BadRequest("Failed to create reservation.")


class CustomerReservation(APIView):
    def __init__(self):
        self.reservation_service = ReservationService()

    def get(self, request, reservation_id, customer_id):
        reservation = self.reservation_service.get_customer_reservation(reservation_id, customer_id)
        reservations_serializer = CustomerReservationResponseSerializer(reservation)

        return Response(reservations_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, customer_id, reservation_id):

        result = self.reservation_service.delete(reservation_id, customer_id)
        if result:
            return Response({"message": "Reservation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            raise BadRequest("Failed to delete this reservation.")

    def put(self, request, customer_id, reservation_id):

        data = request.data
        serializer = CreateReservationSerializer(data=data)
        serializer.is_valid_raise()

        result = self.reservation_service.update_by_customer(reservation_id, customer_id, serializer)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            raise BadRequest("Failed to update this reservation.")


class WorkerReservations(APIView):
    def __init__(self):
        self.reservation_service = ReservationService()

    def get(self, request, worker_id):
        reservations = self.reservation_service.get_worker_reservations(worker_id)
        reservations_serializer = WorkerReservationResponseSerializer(reservations, many=True)

        return Response(reservations_serializer.data, status=status.HTTP_200_OK)


class WorkerReservation(APIView):
    def __init__(self):
        self.reservation_service = ReservationService()

    def get(self, request, reservation_id, worker_id):
        reservation = self.reservation_service.get_worker_reservation(reservation_id, worker_id)
        reservations_serializer = WorkerReservationResponseSerializer(reservation)

        return Response(reservations_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, reservation_id, worker_id):
        data = request.data
        serializer = UpdateReservationByWorkerSerializer(data=data)
        serializer.is_valid_raise()

        result = self.reservation_service.update_by_worker(reservation_id, worker_id, serializer)

        reservations_response_serializer = WorkerReservationResponseSerializer(result, many=True)
        if result:
            return Response(reservations_response_serializer.data, status=status.HTTP_200_OK)
        else:
            raise BadRequest("Failed to update this reservation.")


class CustomerReview(APIView):
    def __init__(self):
        self.review_service = ReviewService()

    def get(self, request, customer_id, reservation_id):
        result = self.review_service.get(customer_id, reservation_id)
        serializer = GetCustomerReviewSerializer(result)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, customer_id, reservation_id):
        data = request.data
        serializer = ReviewSerializer(data=data)
        serializer.is_valid_raise()
        result = self.review_service.create(customer_id, reservation_id, serializer)

        if result == "invalid_status":
            raise BadRequest("Cannot review. Reservation is either pending or rejected.")
        elif result == "exists":
            raise BadRequest("Review already exists! You can update it.")
        else:
            return Response({"review_id": result}, status=status.HTTP_200_OK)

    def put(self, request, customer_id, reservation_id):
        data = request.data
        serializer = ReviewSerializer(data=data)
        serializer.is_valid_raise()
        result = self.review_service.update(customer_id, reservation_id, serializer)

        if result == "invalid_status":
            raise BadRequest("Cannot review. Reservation is either pending or rejected.")
        else:
            return Response({"review_id": result}, status=status.HTTP_200_OK)

    def delete(self, request, customer_id, reservation_id):
        result = self.review_service.delete(customer_id, reservation_id)
        if result:
            return Response({"message": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        raise BadRequest("Failed to delete this review.")


class WorkerReviews(APIView):
    def __init__(self):
        self.review_service = ReviewService()

    def get(self, request, worker_id):
        result = self.review_service.get_worker_reviews(worker_id)
        serializer = GetWorkerReviewsSerializer(result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
