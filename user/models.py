from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import UserManager


class User(AbstractUser):
    first_name = None
    last_name = None
    # Mandatory fields to prevent duplication user
    username = models.CharField(max_length=255, unique=True)
    ktp_id = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, unique=True)

    # Helper fields
    account_no = models.CharField(max_length=255, unique=True, blank=True, null=True)
    balance = models.IntegerField(default=0)
    is_advisor = models.BooleanField(default=False)
    birth_date = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(default=1)
    token = models.CharField(max_length=500, null=True, blank=True) # assuming the token is stored here

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username


class Expertise(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Availability(models.Model):
    time = models.DateTimeField()

    def __str__(self):
        return self.time.strftime("%m/%d/%Y, %H:%M:%S")


class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="advisor", primary_key=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.TextField(default="")
    years_of_experience = models.IntegerField(default=0)
    current_role = models.CharField(max_length=255, blank=True, null=True)
    current_employer = models.CharField(max_length=255, blank=True, null=True)
    rate_per_hour = models.IntegerField(default=0)
    expertise = models.ManyToManyField(Expertise)
    availability = models.ManyToManyField(Availability)

    def __str__(self):
        return self.user.username


