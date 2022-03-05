from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

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
    # max_users_gym = models.IntegerField(default=4)

    def __str__(self):
        return f'Condo Name: {self.name}   Address: {self.address}'


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11)
    user_type = models.CharField(max_length=2, choices=USER_TYPE, default='RU')
    user_status = models.CharField(max_length=1, choices=USER_STATUS_TYPE, default='A')
    address = models.CharField(max_length=100)
    # condo = models.ForeignKey(Condo, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth'] #TODO: verify which is important

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class SignupCode(models.Model):
    code = models.CharField(max_length=128)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    use_status = models.BooleanField(default=False)


class GymSession(models.Model):
    checkin_code = models.CharField(max_length=128, default=128 * '0')
    session_datetime = models.DateTimeField()
    booked_user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    booking_status = models.CharField(max_length=1, choices=BOOKING_STATUS_TYPE, default='B')

    def __str__(self):
        return f'Day {self.session_datetime} Time: User {str(self.booked_user)}'


class Penalties(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stall Number: {self.stall_number}   User: {str(self.user)}'


class VisitorParking(models.Model):
    stall_number = models.IntegerField()
    responsible_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    visitor_name = models.CharField(max_length=64)
    visitor_phone = models.CharField(max_length=11)

    def __str__(self):
        return f'Stall Number: {self.stall_number}   User: {str(self.responsible_user)}'


class TennisCourt(models.Model):
    court_number = models.IntegerField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Court Number: {self.court_number}   User: {str(self.user)}'

