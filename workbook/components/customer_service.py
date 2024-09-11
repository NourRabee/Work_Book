from django.shortcuts import get_object_or_404
from workbook.models.models import Customer
from workbook.serializers.customer_serializer import CustomerUserSerializer, CustomerDetailsSerializer


class CustomerService:

    def update(self, customer_serializer, customer_id):
        validated_data = customer_serializer.validated_data

        customer = Customer.objects.get(id=customer_id)

        customer.user.profile_picture = validated_data['profile_picture']
        customer.user.biography = validated_data['biography']

        customer.save()
        customer.user.save()

        return CustomerUserSerializer(customer).data

    def get(self, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerDetailsSerializer(customer)

        return serializer.data

    def delete(self, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)

        customer.user.delete()
        customer.delete()

        return "Customer deleted successfully."
