from django.db.models import Prefetch, ExpressionWrapper, F, IntegerField, Q
from django.db.models.functions import Concat
from django.db.models import Value

from workbook.components.image_service import ImageService
from workbook.serializers.worker_serializer import *


class WorkerService:
    def __init__(self):
        self.image_service = ImageService()

    def update(self, worker_serializer, worker_id):
        validated_data = worker_serializer.validated_data

        worker = Worker.objects.select_related('user').only(
            'job_title', 'day_start_time', 'day_end_time',
            'user__id', 'user__email', 'user__profile_picture', 'user__biography', 'user__first_name', 'user__last_name'
        ).get(id=worker_id)

        worker.user.profile_picture = validated_data['profile_picture']
        worker.user.biography = validated_data['biography']
        worker.job_title = validated_data['job_title']
        worker.day_start_time = validated_data['day_start_time']
        worker.day_end_time = validated_data['day_end_time']

        worker.save(update_fields=['job_title', 'day_start_time', 'day_end_time'])
        worker.user.save(update_fields=['profile_picture', 'biography'])

        return WorkerUserSerializer(worker).data

    def get_skills(self, worker_id):
        skills = Skill.objects.filter(
            workerskill__worker_id=worker_id
        ).distinct()

        return skills

    def get(self, worker_id):
        reservations_prefetch = Prefetch(
            'reservation_set',
            queryset=Reservation.objects.select_related(
                'customer__user',
                'review'
            ),
            to_attr='prefetched_reservations'
        )
        skills_prefetch = Prefetch(
            'workerskill_set',
            queryset=WorkerSkill.objects.select_related('skill').prefetch_related(reservations_prefetch),
            to_attr='prefetched_skills'
        )

        worker = Worker.objects.select_related('user').prefetch_related(skills_prefetch).get(id=worker_id)

        return worker

    def delete(self, worker_id):
        worker = Worker.objects.get(id=worker_id)
        worker.user.delete()

        return True

    def get_profile_picture(self, worker_id):
        worker_profile_picture = Worker.objects.select_related('user').only('user__profile_picture').get(
            id=worker_id).user.profile_picture

        image_format, image = self.image_service.binary_to_image_field(worker_profile_picture)

        return image_format, image

    def search(self, params):
        search_result = self.search_by(params.search_by, params.search_value)
        order_result = self.order_by(search_result, params.order_by, params.order_type)
        filter_result = self.filter_by(order_result, params.filter_by, params.filter_value)
        paginated_result = filter_result[params.limit * params.offset:(params.limit + params.offset)]

        serializer = WorkerUserSerializer(paginated_result, many=True)

        return serializer.data

    def search_by(self, search_by, search_value):
        if search_by == "first_name":
            # icontains in Django is designed to be case-insensitive but does perform a wildcard-like search.
            workers = Worker.objects.filter(user__first_name__icontains=search_value)

        elif search_by == "last_name":
            workers = Worker.objects.filter(user__last_name__icontains=search_value)

        elif search_by == "full_name":
            name_parts = search_value.split(' ', 1)
            if len(name_parts) == 2:
                first_name, last_name = name_parts
                workers = Worker.objects.filter(
                    Q(user__first_name__icontains=first_name) &
                    Q(user__last_name__icontains=last_name)
                )
            else:
                return {"error": "Full name must be in 'First Last' format."}
        else:
            workers = Worker.objects.filter(workerskill__skill_id=search_value)

        return workers

    def order_by(self, workers, order_by, order_type):
        workers = workers.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name')
        )
        return workers

    def filter_by(self, workers, filter_by, filter_value_seconds):
        if not filter_by or not filter_value_seconds:
            return workers

        selected_workers = workers.annotate(
            is_selected=ExpressionWrapper(
                Value(filter_value_seconds) % F('workerskill__time_slot_period'),
                output_field=IntegerField()
            )
        ).filter(is_selected=0)
