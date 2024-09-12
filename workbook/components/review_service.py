from workbook.enums import ReservationStatus
from workbook.models.models import Reservation, Review


class ReviewService:
    def create(self, customer_id, reservation_id, serializer):
        reservation = Reservation.objects.get(id=reservation_id, customer_id=customer_id)
        validated_data = serializer.validated_data

        if not self.is_reservation_valid_for_review(reservation):
            return "invalid_status"
        elif self.exist(customer_id, reservation_id):
            return "exists"

        review = Review.objects.create(
            reservation=reservation,
            stars=validated_data.get('stars'),
            description=validated_data.get('description')
        )
        review.save()

        return review.pk

    def exist(self, customer_id, reservation_id):
        return Review.objects.filter(
            reservation__customer_id=customer_id,
            reservation_id=reservation_id
        ).exists()

    def is_reservation_valid_for_review(self, reservation):
        return reservation.status not in [ReservationStatus.PENDING.value, ReservationStatus.REJECTED.value]

    def update(self, customer_id, reservation_id, serializer):
        reservation = Reservation.objects.get(id=reservation_id, customer_id=customer_id)

        if not self.is_reservation_valid_for_review(reservation):
            return "invalid_status"

        validated_data = serializer.validated_data

        review = Review.objects.get(
            reservation__customer_id=customer_id,
            reservation_id=reservation_id
        )

        review.stars = validated_data.get('stars')
        review.description = validated_data.get('description')
        review.save()

        return review.pk

    def delete(self, customer_id, reservation_id):
        review = Review.objects.filter(
            reservation__customer_id=customer_id,
            reservation_id=reservation_id
        )
        review.delete()

        return True

    def get(self, customer_id, reservation_id):
        return Review.objects.select_related(
            'reservation__worker_skill__skill'
        ).get(
            reservation__customer_id=customer_id,
            reservation_id=reservation_id
        )

    def get_worker_reviews(self, worker_id):
        reservations = Reservation.objects.filter(worker_skill__worker_id=worker_id)
        reviews = Review.objects.filter(reservation__in=reservations)

        return reviews

