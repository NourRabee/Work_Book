from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Value
from django.db.models.functions import Concat

from workbook.serializers.worker_serializer import *


class WorkerService:

    def update(self, worker_serializer, worker_id):
        validated_data = worker_serializer.validated_data

        worker = Worker.objects.get(id=worker_id)

        worker.user.profile_picture = validated_data['profile_picture']
        worker.user.biography = validated_data['biography']
        worker.job_title = validated_data['job_title']
        worker.day_start_time = validated_data['day_start_time']
        worker.day_end_time = validated_data['day_end_time']

        worker.user.save()
        worker.save()

        return WorkerUserSerializer(worker).data

    def get_skills(self, worker_id):
        worker = Worker.objects.get(id=worker_id)
        worker_skills = worker.workerskill_set.all()
        skills = [worker_skill.skill for worker_skill in worker_skills]
        serializer = SkillSerializer(skills, many=True)

        return Response(serializer.data)

    def get(self, worker_id):
        worker = get_object_or_404(Worker, id=worker_id)
        serializer = WorkerDetailsSerializer(worker)

        return serializer.data

    def delete(self, worker_id):
        worker = get_object_or_404(Worker, id=worker_id)

        worker.user.delete()
        worker.delete()

        return "Worker deleted successfully."

    def search_by(self, param_name, value):

        if param_name == "first_name":
            # icontains in Django is designed to be case-insensitive but does perform a wildcard-like search.
            workers = Worker.objects.filter(user__first_name__icontains=value)
        elif param_name == "last_name":

            workers = Worker.objects.filter(user__last_name__icontains=value)

        elif param_name == "job_title":

            workers = Worker.objects.filter(job_title__icontains=value)

        elif param_name == "full_name":
            name_parts = value.split(' ', 1)
            if len(name_parts) == 2:
                first_name, last_name = name_parts
                workers = Worker.objects.filter(
                    Q(user__first_name__icontains=first_name) &
                    Q(user__last_name__icontains=last_name)
                )
            else:
                return {"error": "Full name must be in 'First Last' format."}

        elif param_name == "skill_id":

            workers = Worker.objects.filter(workerskill__skill_id=value)

        serializer = WorkerUserSerializer(workers, many=True)

        return serializer.data

    def order_by(self, order_by=None, order_type=None):

        # The annotate method is used to add extra fields to each object in the queryset based on calculations or
        # aggregations.
        workers = Worker.objects.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name')
        )
        if order_by == "reviews":
            workers = workers.annotate(
                review_count=Count('workerskill__reservation__review')
            ).order_by('-review_count' if order_type == "desc" else 'review_count')

        elif order_by == "reservations":
            workers = workers.annotate(
                reservation_count=Count('workerskill__reservation')
            ).order_by('-reservation_count' if order_type == "desc" else 'reservation_count')

        else:
            workers = workers.order_by('-full_name' if order_type == "desc" else 'full_name')

        serializer = WorkerUserSerializer(workers, many=True)

        return serializer.data