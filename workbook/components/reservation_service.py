import uuid

from django.core.exceptions import BadRequest
from django.db import transaction
from django.db.models import ExpressionWrapper, F, BigIntegerField

from workbook.helpers import time_helper
from workbook.enums import ReservationStatus
from workbook.models.models import Reservation, WorkerSkill


class ReservationService:
    def get_customer_reservations(self, customer_id):
        reservations = (
            Reservation.objects
            .filter(customer_id=customer_id)
            .select_related('worker_skill__worker__user', 'worker_skill__skill')
            .only(
                'worker_skill__worker__user__first_name',
                'worker_skill__worker__user__last_name',
                'start_date_time',
                'status',
                'worker_skill__skill__name',
                'worker_skill__skill__description'
            )
        )

        return reservations

    def create(self, customer_id, serializer):
        reservation_ids = []

        validated_data = serializer.validated_data

        worker_skill = WorkerSkill.objects.select_related('worker').get(id=validated_data['worker_skill_id'])
        worker = worker_skill.worker
        time_slot_period = worker_skill.time_slot_period

        number_of_slots = int(validated_data['reserved_time_in_seconds'] // time_slot_period)

        start_date_time_unix = (validated_data['start_date_time']).timestamp()

        if (self.is_time_reserved(worker.pk, start_date_time_unix, validated_data['reserved_time_in_seconds'])
                or self.is_time_exceeded(worker, start_date_time_unix, validated_data['reserved_time_in_seconds'])):
            return False

        group_id = uuid.uuid1()

        for i in range(number_of_slots):
            validated_data['start_date_time'] = start_date_time_unix
            reservation = Reservation.objects.create(
                worker_skill_id=validated_data['worker_skill_id'],
                start_date_time=start_date_time_unix,
                time_slot_period=time_slot_period,
                status=ReservationStatus.PENDING.value,
                customer_id=customer_id,
                group_id=group_id

            )
            reservation.save()
            reservation_ids.append(reservation.pk)
            start_date_time_unix += time_slot_period

        return {"ids": reservation_ids}

    def is_time_reserved(self, worker_id, start_date_time_unix, reserved_time_in_seconds):
        end_date_time_unix = start_date_time_unix + reserved_time_in_seconds

        reservations = Reservation.objects.annotate(
            reservation_end=ExpressionWrapper(
                F('start_date_time') + F('time_slot_period'),
                output_field=BigIntegerField()
            )
        ).filter(
            worker_skill__worker_id=worker_id,
            start_date_time__lt=end_date_time_unix,
            reservation_end__gt=start_date_time_unix
        )

        return reservations.exists()

    def is_time_exceeded(self, worker, start_date_time_unix, reserved_time_in_seconds):
        end_date_time_unix = start_date_time_unix + reserved_time_in_seconds

        reservation_start_time = time_helper.extract_time_from_unix(start_date_time_unix)
        reservation_end_time = time_helper.extract_time_from_unix(end_date_time_unix)

        if reservation_start_time < worker.day_start_time or reservation_end_time > worker.day_end_time:
            return True

        return False

    def get_customer_reservation(self, reservation_id, customer_id):
        reservation = (
            Reservation.objects
            .filter(id=reservation_id, customer_id=customer_id)
            .select_related('worker_skill__worker__user', 'worker_skill__skill')
            .only(
                'worker_skill__worker__user__first_name',
                'worker_skill__worker__user__last_name',
                'start_date_time',
                'status',
                'worker_skill__skill__name',
                'worker_skill__skill__description'
            ).first()
        )
        return reservation

    def delete(self, reservation_id, customer_id):

        reservation = Reservation.objects.get(id=reservation_id, customer_id=customer_id)

        if reservation.status != ReservationStatus.PENDING.value:
            return False

        reservations = Reservation.objects.filter(group_id=reservation.group_id)
        reservations.delete()

        return True

    def update_by_customer(self, reservation_id, customer_id, serializer):
        reservation = Reservation.objects.get(id=reservation_id, customer_id=customer_id)
        serializer.validated_data['worker_skill_id'] = reservation.worker_skill_id

        if reservation.status != ReservationStatus.PENDING.value:
            return False

        reservations = Reservation.objects.filter(group_id=reservation.group_id)

        reserved_time_in_seconds = reservations[0].time_slot_period * len(reservations)

        start_date_time = serializer.validated_data.get('start_date_time')
        reserved_time_in_seconds = serializer.validated_data.get('reserved_time_in_seconds', reserved_time_in_seconds)

        if start_date_time and reserved_time_in_seconds:
            serializer.validated_data['start_date_time'] = start_date_time
            serializer.validated_data['reserved_time_in_seconds'] = reserved_time_in_seconds
            return self.update_implementation(customer_id, serializer, reservations)

        elif reserved_time_in_seconds:
            serializer.validated_data['start_date_time'] = reservation.start_date_time
            return self.update_implementation(customer_id, serializer, reservations)

        elif start_date_time:
            serializer.validated_data['reserved_time_in_seconds'] = reserved_time_in_seconds
            return self.update_implementation(customer_id, serializer, reservations)

        return False

    def update_implementation(self, customer_id, serializer, reservations):
        try:
            with transaction.atomic():
                reservations.delete()

                new_reservation_ids = self.create(customer_id, serializer)

                if not new_reservation_ids:
                    raise BadRequest("Couldn't update the reservation.")
                return new_reservation_ids

        except BadRequest as e:
            raise e

    def get_worker_reservations(self, worker_id):
        reservations = (
            Reservation.objects
            .filter(worker_skill__worker_id=worker_id)
            .select_related('customer__user', 'worker_skill__skill')
            .only(
                'customer__user__first_name',
                'customer__user__last_name',
                'start_date_time',
                'status',
                'worker_skill__skill__name',
                'worker_skill__skill__description'
            )
        )
        return reservations

    def get_worker_reservation(self, reservation_id, worker_id):
        reservation = (
            Reservation.objects
            .filter(id=reservation_id, worker_skill__worker_id=worker_id)
            .select_related('customer__user', 'worker_skill__skill')
            .only(
                'customer__user__first_name',
                'customer__user__last_name',
                'start_date_time',
                'status',
                'worker_skill__skill__name',
                'worker_skill__skill__description'
            ).first()
        )
        return reservation

    def update_by_worker(self, reservation_id, worker_id, serializer):
        reservation = Reservation.objects.get(id=reservation_id, worker_skill__worker_id=worker_id)

        Reservation.objects.filter(group_id=reservation.group_id).update(status=serializer.validated_data['status'])

        return Reservation.objects.filter(group_id=reservation.group_id)
