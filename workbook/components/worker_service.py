from django.db.models import Q, Count, ExpressionWrapper, F, IntegerField, Func
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

        return selected_workers
