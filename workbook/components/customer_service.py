from django.db.models import Prefetch

from workbook.components.image_service import ImageService
from workbook.models.models import Customer, Reservation
from workbook.serializers.customer_serializer import CustomerUserSerializer


class CustomerService:
    def __init__(self):
        self.image_service = ImageService()

    def update(self, customer_serializer, customer_id):
        validated_data = customer_serializer.validated_data

        customer = (Customer.objects.select_related('user').
                    only('user__first_name', 'user__last_name', 'user__email',
                         'user__profile_picture', 'user__biography').get(id=customer_id))

        customer.user.profile_picture = validated_data['profile_picture']
        customer.user.biography = validated_data['biography']

        customer.user.save(update_fields=['profile_picture', 'biography'])

        return CustomerUserSerializer(customer).data

    def get(self, customer_id):

        reservations_prefetch = Prefetch(
            'reservation_set',
            queryset=Reservation.objects.select_related(
                'worker_skill__worker__user',
                'worker_skill__skill',
                'review'
            ),to_attr='prefetched_reservations'
        )

        customer = Customer.objects.select_related('user').prefetch_related(reservations_prefetch).get(id=customer_id)

        return customer

    def delete(self, customer_id):
        customer = Customer.objects.get(id=customer_id)
        customer.user.delete()

        return True

    def get_profile_picture(self, customer_id):
        customer_profile_picture = Customer.objects.select_related('user').only('user__profile_picture').get(
            id=customer_id).user.profile_picture

        image_format, image = self.image_service.binary_to_image_field(customer_profile_picture)

        return image_format, image
