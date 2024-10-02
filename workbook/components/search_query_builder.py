from django.core.exceptions import BadRequest
from django.db.models import Q, Count
from django.db.models.functions import Concat
from django.db.models import Value
from workbook.models.models import Worker
from workbook.serializers.worker_serializer import WorkerUserSerializer


class SearchQueryBuilder:
    def __init__(self):
        self.queryset = Worker.objects.all()
        self.params = None

    def set_params(self, params):
        self.params = params
        return self

    def build_search_by(self):
        if self.params.search_by == "first_name":
            self.queryset = self.queryset.filter(user__first_name__icontains=self.params.search_value)

        elif self.params.search_by == "last_name":
            self.queryset = self.queryset.filter(user__last_name__icontains=self.params.search_value)

        elif self.params.search_by == "full_name":
            name_parts = self.params.search_value.split(' ', 1)
            if len(name_parts) == 2:
                first_name, last_name = name_parts
                self.queryset = self.queryset.filter(
                    Q(user__first_name__icontains=first_name) & Q(user__last_name__icontains=last_name)
                )
            else:
                raise BadRequest("Full name must be in 'First Last' format.")

        elif self.params.search_by == "skill_id":
            self.queryset = self.queryset.filter(workerskill__skill_id=self.params.search_value)

        return self

    def build_order_by(self):
        # Annotate full name to be used for ordering if necessary
        self.queryset = self.queryset.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name')
        )

        if self.params.order_by == "reviews":
            self.queryset = self.queryset.annotate(
                review_count=Count('workerskill__reservation__review')
            ).order_by('-review_count' if self.params.order_type == "desc" else 'review_count')

        elif self.params.order_by == "reservations":
            self.queryset = self.queryset.annotate(
                reservation_count=Count('workerskill__reservation')
            ).order_by('-reservation_count' if self.params.order_type == "desc" else 'reservation_count')

        else:
            self.queryset = self.queryset.order_by('-full_name' if self.params.order_type == "desc" else 'full_name')

        return self

    def build_filter(self):
        if self.params.filter_value:
            self.queryset = self.queryset.filter(
                workerskill__time_slot_period=self.params.filter_value
            ).distinct()

        return self

    def paginate(self):
        start = self.params.limit * self.params.offset
        end = start + self.params.limit
        self.queryset = self.queryset[start:end]
        return self

    def execute(self):
        serializer = WorkerUserSerializer(self.queryset, many=True)
        return serializer.data
