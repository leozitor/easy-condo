from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, AbstractUser

USER_TYPE = (
    ('RU', 'Resident User'),
    ('AD', 'Administrator'),
    ('SP', 'Service Provider')
)

BOOKING_STATUS_TYPE = (
    ('B', 'Booked'),
    ('C', 'Canceled'),
    ('M', 'Missed')
)

USER_STATUS_TYPE = (
    ('A', 'Active'),
    ('P', 'Penalized'),
    ('I', 'Inactive')
)


class Condo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Condo Name: {self.name}   Address: {self.address}'


class UserProfile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=11)
    user_type = models.CharField(max_length=2, choices=USER_TYPE, default='RU')
    user_status = models.CharField(max_length=1, choices=USER_STATUS_TYPE, default='A')
    address = models.CharField(max_length=100)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Username: {self.user.username}   Name: {self.user.first_name + self.user.last_name}'


# class User(AbstractUser):
#     GENDER = (
#         ('M', 'Male'),
#         ('F', 'Female')
#     )
#
#     gender = models.CharField(max_length=1, choices=GENDER)
#     birthday = models.DateField()
#     phone_number = models.CharField(max_length=11)
#     user_type = models.CharField(max_length=2, choices=USER_TYPE, default='RU')
#     user_status = models.CharField(max_length=1, choices=USER_STATUS_TYPE, default='A')
#     address = models.CharField(max_length=100)
#     condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'Username: {self.username}   Name: {self.first_name + self.last_name}'
#
# And in your settings.py.
#
# AUTH_USER_MODEL = 'users.User'


class SignupCode(models.Model):
    code = models.CharField(max_length=128)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    use_status = models.BooleanField(default=False)


class GymSession(models.Model):
    checkin_code = models.CharField(max_length=128, default=128 * '0')
    day = models.DateField()
    time = models.TimeField()
    booked_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    booking_status = models.CharField(max_length=1, choices=BOOKING_STATUS_TYPE, default='B')

    def __str__(self):
        return f'Day {self.day} Time: {self.time} User {str(self.booked_user)}'


class Penalties(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    penalty_amount = models.IntegerField()
    penalty_reason = models.CharField(max_length=100)
    penalty_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User: {str(self.user)}   Amount: {self.penalty_amount}   Reason: {self.penalty_reason}'


class CondoParking(models.Model):
    stall_number = models.IntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stall Number: {self.stall_number}   User: {str(self.user)}'


class VisitorParking(models.Model):
    stall_number = models.IntegerField()
    responsible_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    visitor_name = models.CharField(max_length=64)
    visitor_phone = models.CharField(max_length=11)

    def __str__(self):
        return f'Stall Number: {self.stall_number}   User: {str(self.responsible_user)}'


class TennisCourt(models.Model):
    court_number = models.IntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Court Number: {self.court_number}   User: {str(self.user)}'

