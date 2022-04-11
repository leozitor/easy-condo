from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

USER_TYPE = (
    ('RU', 'Resident User'),
    ('CA', 'Condo Admin'),
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

SIGNUP_TYPE = (
    ('U', 'Used'),
    ('A', 'Available')
)

STALL_TYPE = (
    ('V', 'VISITOR'),
    ('R', 'RESIDENT')
)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'Not Applicable')
)


class Condo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # max_users_gym = models.IntegerField(default=4)

    def __str__(self):
        return f'Condo Name: {self.name}   Address: {self.address}'


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
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
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11)
    user_type = models.CharField(max_length=2, choices=USER_TYPE, default='RU')
    user_status = models.CharField(max_length=1, choices=USER_STATUS_TYPE, default='A')
    address = models.CharField(max_length=100, null=True)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=1, choices=GENDER)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['date_of_birth'] #TODO: verify which is important

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
    code = models.CharField(max_length=36)
    condo_id = models.ForeignKey(Condo, on_delete=models.CASCADE, null=True)  # TODO: change to null=False
    use_status = models.CharField(max_length=1, choices=SIGNUP_TYPE, default='A')


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


class Stall(models.Model):
    stall_label = models.CharField(max_length=8)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    stall_type = models.CharField(max_length=1, choices=STALL_TYPE, default='V')

    def __str__(self):
        return f'Stall: {self.stall_label} Type: {self.stall_type}  on Condo: {str(self.condo)}'


class StallReservation(models.Model):
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateField()

    # status = models.CharField(max_length=1, choices=STALL_STATUS_TYPE, default='C')

    def __str__(self):
        return f'Stall: {self.stall} Reserved for user {self.user}  checkin on Date: {self.date}'


class TennisCourt(models.Model):
    court_number = models.IntegerField()
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    time_slot = models.TimeField()

    def __str__(self):
        return f'Court Number: {self.court_number}, Condo: {str(self.condo.name)}, on time slot: {str(self.time_slot)}'


class TennisCourtReservation(models.Model):
    court = models.ForeignKey(TennisCourt, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateField()

    # status = models.CharField(max_length=1, choices=STALL_STATUS_TYPE, default='C')

    def __str__(self):
        return f'Court: {self.court} Reserved for user {self.user}  on Time : {self.date}'


class PartyRoom(models.Model):
    room_name = models.CharField(max_length=16)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Room Name: {self.room_name}   Condo: {str(self.condo.name)}'


class PartyRoomReservation(models.Model):
    party_room = models.ForeignKey(PartyRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'Party Room: {self.party_room} Reserved for user {self.user}  on Date: {self.date}'
