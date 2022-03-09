from datetime import datetime, timezone, date, timedelta
from itertools import chain
import json
import pandas as pd
import uuid

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .admin import UserCreationForm
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from webapp.forms import *
from webapp.models import *
from webapp.admin import *

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


def condo_signup(request):
    if request.method == 'POST':
        form = CondoCreationForm(request.POST)
        if form.is_valid():
            condo = form.save()
            # log the user in
            return redirect('index')
    else:
        form = CondoCreationForm()
    return render(request, "condo_signup.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('user_dashboard')
                else:
                    return redirect('index')
        else:
            return redirect('index')
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def activity(request, activity):
    if activity == 'gym':
        return render(request, 'calendar_dashboard.html',
                      {'user_schedule': user_schedule(request)})

    if activity == 'parking':
        user = MyUser.objects.get(email=request.user)
        #condo = user.condo
        #visitor_stalls = VisitorParking.objects.filter(condo=condo)
        dummy_data = [
                       [{"id": 0, "label": "stall 1", "hour": 0, "minute": 0, "day": f'{4+day}', "month": 3, "year": 2022,
                        "count": 0},
                       {"id": 0, "label": "stall 2", "hour": 6, "minute": 30, "day":f'{4+day}', "month": 3, "year": 2022,
                        "count": 0},
                       {"id": 0, "label": "stall 3", "hour": 7, "minute": 0, "day": f'{4+day}', "month": 3, "year": 2022,
                        "count": 0},
                       {"id": 0, "label": "stall 4", "hour": 7, "minute": 30, "day":f'{4+day}', "month": 3, "year": 2022,
                        "count": 0},
                       {"id": 0, "label": "stall 5", "hour": 8, "minute": 0, "day": f'{4+day}', "month": 3, "year": 2022,
                        "count": 0}]
            for day in range(0,7)]
        dummy_data = sum(dummy_data, [])

        return render(request, 'activity_calendar.html', {'activity_name': activity, 'activity_slots': json.dumps(dummy_data)})

    return render(request, 'calendar.html')


def code_generator(n):
    return [uuid.uuid1() for i in range(n)]


@login_required
def user_dashboard(request):
    options = ['gym', 'parking', 'setting', 'tennis', 'party', 'visitors']
    return render(request, 'user_dashboard.html', {'options': options})


@login_required
def gym_session_calendar(request):
    calendar = schedule()
    return render(request, 'calendar.html',
                  {'activity_name': activity, 'elements': [1, 2, 3, 4, 5, 6], 'calendar': calendar})


@login_required
def activity_calendar(request):
    return render(request, 'activity_calendar.html',{'activity_name': activity, 'elements': [1, 2, 3, 4, 5, 6], 'calendar': calendar})


@login_required
def add_booking(request):
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
def delete_booking(request):
    ts_id = request.POST['id']  # training session booking id
    GymSession.objects.filter(id=ts_id).delete()
    return render(request, 'calendar_dashboard.html', context={'user_schedule': user_schedule(request)})


@login_required #TODO: change for staff
def generate_codes(request):
    if request.method == 'POST':
        codes = code_generator(int(request.POST['quantity']))
        print(str(codes))  # TODO: send remove
        for code in codes:
            SignupCode.objects.create(code=code)
        return render(request, 'code_generator.html', context={'codes': codes})
    else:
        return render(request, 'code_generator.html')


@login_required
#  making one temporal view request for coding user dashboard
def calendar(request):
    return render(request, 'calendar.html')