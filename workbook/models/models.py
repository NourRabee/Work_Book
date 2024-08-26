from django.db import models
from django.utils import timezone

from workbook.enums import ReservationStatus, MessageSender, UserType


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    salt = models.CharField(max_length=29)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    biography = models.TextField(null=True, blank=True)
    role = models.CharField(choices=UserType.choices(), default=UserType.CUSTOMER, max_length=29)


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    day_start_time = models.IntegerField(help_text="Duration of the time slot in seconds", null=True, blank=True)
    day_end_time = models.IntegerField(help_text="Duration of the time slot in seconds", null=True, blank=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class WorkerSkill(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    time_slot_period = models.IntegerField(help_text="Duration of the time slot in seconds")


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker_skill = models.ForeignKey(WorkerSkill, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(null=True, blank=True)
    time_slot_period = models.IntegerField(null=True, blank=True, help_text="Duration of the time slot in seconds")

    status = models.CharField(choices=ReservationStatus.choices(), default=ReservationStatus.IN_PROGRESS, max_length=29)


class Review(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    stars = models.IntegerField()
    description = models.TextField()


class Chat(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(choices=MessageSender.choices(), default=MessageSender.CUSTOMER, max_length=29)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=300, unique=True)
    token_start_time = models.DateTimeField(default=timezone.now)
