from django.shortcuts import get_object_or_404
from rest_framework.response import Response

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
