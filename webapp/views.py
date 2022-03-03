from datetime import datetime, timezone, date, timedelta
from itertools import chain
import json
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .admin import UserCreationForm
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from webapp.forms import *
from webapp.models import *


def prepare_schedule():
    # available schedule -> period [StartHour, EndHour]
    DAYS_ADVANCE = 7  # number of days of querying the calendar in advance

    period = {'morning': [6, 12], 'afternoon': [16, 22]}

    morning = range(period['morning'][0], period['morning'][1])
    afternoon = range(period['afternoon'][0], period['afternoon'][1])

    # sessions of 30 minutes starting at 00 and 30
    hour = pd.DataFrame({'hour': chain(morning, afternoon)})
    minute = pd.DataFrame({'minute': [0, 30]})

    base = datetime.today() + timedelta(days=1)
    days = pd.DataFrame({'datetime': [base + timedelta(days=x) for x in range(DAYS_ADVANCE)]})
    schedule = hour.merge(minute, how='cross').merge(days, how='cross')

    schedule['day'] = schedule['datetime'].apply(lambda s: s.day)
    schedule['month'] = schedule['datetime'].apply(lambda s: s.month)
    schedule['year'] = schedule['datetime'].apply(lambda s: s.year)

    # rearranging columns order
    schedule = schedule[['hour', 'minute', 'day', 'month', 'year', 'datetime']]

    # fixing time format
    schedule['datetime'] = schedule.apply(
        lambda dt: dt['datetime'].replace(hour=dt['hour'], minute=dt['minute'], second=0, microsecond=0), axis=1)

    return schedule

def add_pd_datetime(df):
    df['session_datetime'] = pd.to_datetime(df['session_datetime'])

    df['year'] = df['session_datetime'].dt.year
    df['month'] = df['session_datetime'].dt.month
    df['day'] = df['session_datetime'].dt.day
    df['hour'] = df['session_datetime'].dt.hour
    df['minute'] = df['session_datetime'].dt.minute


def user_schedule(request):
    user = MyUser.objects.get(email=request.user)
    query = GymSession.objects.filter(booked_user=user)
    if query.exists():
        df = pd.DataFrame(list(query.values()))
        add_pd_datetime(df)
        df = df[['id', 'hour', 'minute', 'day', 'month', 'year']]
        return json.dumps(df.to_dict(orient='records'))
    else:
        return None


def query_schedule():
    dt = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    query = GymSession.objects.filter(session_datetime__gte=dt)
    if query.exists():
        df = pd.DataFrame(list(query.values()))
        add_pd_datetime(df)
        return df
    else:
        return None


def schedule():
    schedule = prepare_schedule()
    df = query_schedule()
    if df is not None:
        calendar = pd.merge(schedule, df, how='left', on=['hour', 'minute', 'day'], suffixes=('', '_y')).drop(
            columns=['year_y', 'month_y'])

        count = calendar.groupby(['hour', 'minute', 'day']).count().reset_index().rename(
            columns={'booked_user_id': 'count'})
        count = pd.merge(schedule, count[['hour', 'minute', 'day', 'count', 'id']], how='left',
                         on=['hour', 'minute', 'day'],
                         suffixes=('', '_y'))
        count = count[['id', 'hour', 'minute', 'day', 'month', 'year', 'count']].sort_values(
            ['day', 'hour', 'minute']).reset_index(drop=True)

        data = count.to_dict(orient='records')

        return json.dumps(data)
    else:
        return None


def index(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        return redirect('user_login')


# @require_http_methods(["POST"])
# def login(request):
#     auth_form = AuthenticationForm(request, data=request.POST)
#     if auth_form.is_valid():
#         username = auth_form.cleaned_data.get('username')
#         password = auth_form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, 'user_dashboard.html', context=data)
#         else:
#             return render(request, 'error_404.html')
#     else:
#         return render(request, 'error_404.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {'form': form, 'user_logged': True})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def activity(request, activity):
    if activity == 'gym':
        calendar = schedule()
        return render(request, 'calendar.html', {'activity_name': activity, 'elements': [1, 2, 3, 4, 5, 6], 'calendar': calendar})
    if activity == 'parking':
        user = MyUser.objects.get(email=request.user)
        #condo = user.condo
        #visitor_stalls = VisitorParking.objects.filter(condo=condo)
        return render(request, 'activity_calendar.html', {'activity_name': activity, 'parking':[1,2,3,4,5,6]})
    return render(request, 'calendar.html')


@login_required
def user_dashboard(request):
    options = ['gym', 'parking', 'setting', 'tennis', 'party', 'visitors']
    return render(request, 'user_dashboard.html', {'options': options})


@login_required
def calendar_dashboard(request):
    return render(request, 'calendar_dashboard.html', {'user_schedule': user_schedule(request)})


@login_required
def add_booking(request):  # TODO build this
    dt_str = request.POST['timeStamp']  # datetime string
    dt = datetime.strptime(dt_str, "%m/%d/%Y, %H:%M").replace(tzinfo=timezone.utc)
    user = MyUser.objects.get(email=request.user)
    count_ts = GymSession.objects.filter(session_datetime=dt).count()  # Number of Training Sessions same Time
    # User can't book more than one session at the same day
    cur_day = datetime.strptime(dt_str, "%m/%d/%Y, %H:%M").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    after_day = cur_day + timedelta(days=1)
    user_ct = GymSession.objects.filter(session_datetime__gte=cur_day, session_datetime__lt=after_day, booked_user=user).count()
    if count_ts < 4 and user_ct < 1:#TODO: insert based on the condo
        GymSession.objects.create(session_datetime=dt, booked_user=user)
        return render(request, 'calendar.html', context={'calendar': schedule()})
    else:
        return render(request, 'calendar.html', context={'calendar': schedule()})


@login_required
def delete_booking(request):  # TODO build this
    ts_id = request.POST['id']  # training session booking id
    GymSession.objects.filter(id=ts_id).delete()  # TODO: can be changed only the status instead of removal
    return render(request, 'calendar_dashboard.html', context={'user_schedule': user_schedule(request)})

@login_required
#  making one temporal view request for coding user dashboard
def calendar(request):
    return render(request, 'calendar.html')