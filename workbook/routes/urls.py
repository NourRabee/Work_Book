from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from workbook.views.views import *

urlpatterns = \
    [
        path('signin', SignInView.as_view()),
        path('signup', SignUpView.as_view()),

        path('workers/<int:worker_id>', Worker.as_view()),

        path('workers/search', SearchWorkers.as_view()),

        path('customers/<int:customer_id>', Customer.as_view()),

        path('workers/<int:worker_id>/skills', WorkerSkills.as_view()),

        path('customers/<int:customer_id>/reservations', CustomerReservationsView.as_view()),
        path('customers/<int:customer_id>/reservations/<int:reservation_id>', CustomerReservationView.as_view()),

        path('workers/<int:worker_id>/reservations', WorkerReservationsView.as_view()),
        path('workers/<int:worker_id>/reservations/<int:reservation_id>', WorkerReservationView.as_view())

    ] + debug_toolbar_urls()
