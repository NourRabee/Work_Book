from django.db.models import Prefetch
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