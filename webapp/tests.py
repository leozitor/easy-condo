from datetime import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from django.test import Client
# Create your tests here.

# create an instance of the client for our use
from webapp.models import *


class UserTest(TestCase):
    def test_public_endpoints(self):
        urls = ['/', '/signup', '/condo_signup', '/user_login']
        for url in urls:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_logged_reguired_get_urls(self):
        urls = ['/user_dashboard/', '/gym_session_calendar/']
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)

    def test_create_user(self):
        self.user = MyUser.objects.create_user(email='user@gmail.com', password='123456')
        login = self.client.login(email='user@gmail.com', password='123456')
        self.assertTrue(login)

    def test_user_logout(self):
        self.user = MyUser.objects.create_user(email='user@gmail.com', password='123456')
        self.client.login(email='user@gmail.com', password='123456')
        response = self.client.get('/user_logout/', follow=True)
        self.assertEqual(response.status_code, 200)

    # def test_user_dashboard(self):
    #     self.user = MyUser.objects.create_user(email='user@gmail.com', password='123456')
    #     self.client.login(email='user@gmail.com', password='123456')
    #     response = self.client.post('add_booking/', {'timeStamp': '03/30/2022, 07:00'}, follow=True)
    #     print(response)





class BookingTest(TestCase):

    def test_training_session_creation(self):
        self.user = MyUser.objects.create_user(email='user@gmail.com', password='123456')
        self.client.login(email='user@gmail.com', password='123456')
        dt = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        GymSession.objects.create(session_datetime=dt, booked_user=self.user)

        self.assertEqual(len(GymSession.objects.all()), 1)


    # def test_training_session_creation_with_same_day(self):
    #     self.user = MyUser.objects.create_user(email='user@gmail.com', password='123456')
    #     self.client.login(email='user@gmail.com', password='123456')
    #     dt = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    #     response = self.client.post('add_booking/', {'timeStamp':  '03/29/2022, 08:00'}, follow=True)
    #     print(response)
    #     GymSession.objects.create(session_datetime=dt, booked_user=self.user)
    #     print(GymSession.objects.all())
    #     self.assertEqual(len(GymSession.objects.all()), 1)


