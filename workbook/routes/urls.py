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

        path('customers/<int:customer_id>/reservations', CustomerReservations.as_view()),  # get customer's reservations --> no body
        # delete customer's reservation (in progress, completed = no delete, pending
        # ask about put,
        # create a new reservation, validation on start_date_time must be in future but between start_time and end_time of worker time

        path('workers/<int:worker_id>/reservations', WorkerReservations.as_view()) #get worker's reservations, #put -> change status of reservations


    ] + debug_toolbar_urls()
