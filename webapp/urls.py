from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('<str:message>', views.message, name='message'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_dashboard/<str:activity_type>', views.activity_dashboard, name='activity_dashboard'),
    path('delete_activity_reservation/<str:activity_type>', views.delete_activity_reservation, name='delete_activity_reservation'),
    path('add_booking/', views.add_booking, name='add_booking'),
    path('add_booking_activity/<str:activity>', views.add_booking_activity, name='add_booking_activity'),
    path('delete_booking/', views.delete_booking, name='delete_booking'),
    path('gym_session_calendar/', views.gym_session_calendar, name='gym_session_calendar'),
    path('activity_calendar/<str:activity_type>', views.activity_calendar, name='activity_calendar'),
    path('generate_codes/', views.generate_codes, name='generate_codes'),
    path('generate_codes/download_csv/', views.download_csv, name='download_csv')
]