from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_dashboard/<str:activity>', views.activity, name='dashboard_activity'),
    path('add_booking/', views.add_booking, name='add_booking'),
    path('delete_booking/', views.delete_booking, name='delete_booking'),
    path('condo_signup/', views.condo_signup, name='condo_signup'),
    path('gym_session_calendar/', views.gym_session_calendar, name='gym_session_calendar'),
    path('activity_calendar/', views.activity_calendar, name='activity_calendar'),
    path('generate_codes/', views.generate_codes, name='generate_codes'),
]