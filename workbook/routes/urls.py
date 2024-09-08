from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from workbook.models.models import *
from workbook.views.views import *

urlpatterns = \
    [
        path('signin', SignInView.as_view()),
        path('signup', SignUpView.as_view()),

        path('workers/<int:worker_id>', Worker.as_view()),
        path('workers/<int:worker_id>/profile-picture', WorkerProfilePicture.as_view()),


        path('customers/<int:customer_id>', Customer.as_view()),
        path('customers/<int:customer_id>/profile-picture', CustomerProfilePicture.as_view()),

        # path('users/<int:user_id>/profile-picture', Worker.as_view()),


        path('workers/<int:worker_id>/skills', WorkerSkills.as_view()),

    ] + debug_toolbar_urls()
