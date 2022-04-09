from datetime import datetime, timezone, date, timedelta, time
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

messages = {'sucess_account': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                               'message': 'Account created successfully.'},
            'sucess_login': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                             'message': 'Login successful.'},
            'error_email': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger',
                            'message': 'E-mail already registered'},
            'invalid_email': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Invalid Email !'},
            'error_password': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Wrong password!'},
            }


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


def split_time(df, col):
    df['hour'] = df[col].apply(lambda s: s.hour)
    df['minute'] = df[col].apply(lambda s: s.minute)
    df['time'] = df[col].apply(lambda s: time(hour=s.hour, minute=s.minute))
    return df


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


def prepareActivitySchedule(cur_date, activityRoomQuery, activityReservationQuery, type, activity_id, qtlimit, group):
    data = []
    for day in [cur_date + timedelta(days=x) for x in range(7)]:
        rooms = pd.DataFrame(list(activityRoomQuery.values()))
        reservations = activityReservationQuery.values()
        if not reservations.exists():
            reservations = pd.DataFrame({activity_id: [], 'user_id': []})
        else:
            reservations = pd.DataFrame(list(reservations))
        rooms = rooms.merge(reservations, left_on='id', right_on=activity_id, how='left', suffixes=('', '_y')).groupby(
            group).count()['user_id'].reset_index().rename(
            columns={'user_id': 'count', 'stall_label': 'label'})
        rooms['day'] = day.day
        rooms['month'] = day.month
        rooms['year'] = day.year
        rooms['hour'] = 0
        rooms['minute'] = 0
        rooms['type'] = type
        rooms['qtlimit'] = qtlimit  # depends on the activity
        data.append(rooms.to_dict(orient='records'))
    data = sum(data, [])
    return data


def reservationExist(queryObj, col_dic):
    if not queryObj.exists():
        return pd.DataFrame(col_dic)
    else:
        return pd.DataFrame(list(queryObj))


def complete_df_to_dict(df, time, type, qtlimit):
    df['day'] = time.day
    df['month'] = time.month
    df['year'] = time.year
    df['type'] = type
    df['qtlimit'] = qtlimit
    if isinstance(time, datetime):
        df['hour'] = time.hour
        df['minute'] = time.minute
    else:
        df['hour'] = 0
        df['minute'] = 0
    return df.to_dict(orient='records')


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
            form = AuthenticationForm()
            return render(request, "login.html", {'form': form, 'alert_msg': messages['error_password']})
            # return redirect('index')
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def admin_dashboard(request):
    return redirect('/admin/')


def activity(request, activity):
    today = datetime.today()
    cur_date = datetime(day=today.day, month=today.month, year=today.year) - timedelta(
        1)  # TODO mudar aqui pra pegar a do dia e quando o usuario pedir
    user = MyUser.objects.get(email=request.user)
    data = []
    if activity == 'gym':
        print(user_schedule(request))
        return render(request, 'calendar_dashboard.html', {'user_schedule': user_schedule(request)})
    elif activity == 'parking':
        for day in [cur_date + timedelta(days=x) for x in range(7)]:
            stalls = pd.DataFrame(list(Stall.objects.filter(condo=user.condo).values()))
            reservations = StallReservation.objects.filter(date=day).values()
            reservations = reservationExist(reservations, {'stall_id': [], 'user_id': []})
            stalls = \
                stalls.merge(reservations, left_on='id', right_on='stall_id', how='left', suffixes=('', '_y')).groupby(
                    ['id', 'stall_label']).count()['user_id'].reset_index().rename(
                    columns={'user_id': 'count', 'stall_label': 'label'})
            data.append(complete_df_to_dict(stalls, day, 'parking', 1))
        stalls_data = sum(data, [])
        return render(request, 'activity_calendar.html',
                      {'activity_name': activity, 'activity_slots': json.dumps(stalls_data)})
    elif activity == 'party':
        for day in [cur_date + timedelta(days=x) for x in range(7)]:
            rooms = pd.DataFrame(list(PartyRoom.objects.filter(condo=user.condo).values()))
            reservations = PartyRoomReservation.objects.filter(day_of_use=day).values()
            reservations = reservationExist(reservations, {'party_room_id': [], 'user_id': []})
            rooms = \
                rooms.merge(reservations, left_on='id', right_on='party_room_id', how='left',
                            suffixes=('', '_y')).groupby(
                    ['id', 'room_name']).count()['user_id'].reset_index().rename(
                    columns={'user_id': 'count', 'room_name': 'label'})
            data.append(complete_df_to_dict(rooms, day, 'party', 1))
        rooms_data = sum(data, [])
        return render(request, 'activity_calendar.html',
                      {'activity_name': activity, 'activity_slots': json.dumps(rooms_data)})
    elif activity == 'tennis':
        for day in [cur_date + timedelta(days=x) for x in range(7)]:
            courts = pd.DataFrame(list(TennisCourt.objects.filter(condo=user.condo).values()))
            reservations = TennisCourtReservation.objects.filter(use_time__gte=day,
                                                                 use_time__lt=(day + timedelta(1))).values()
            reservations = reservationExist(reservations, {'court_id': [], 'user_id': []})
            reservations = split_time(reservations, 'use_time')
            courts = split_time(courts, 'time_slot')
            courts = \
                courts.merge(reservations, left_on=['id', 'hour', 'minute'], right_on=['court_id', 'hour', 'minute'],
                             how='left', suffixes=('', '_y')).groupby(
                    ['id', 'court_number', 'hour', 'minute']).count()['user_id'].reset_index().rename(
                    columns={'user_id': 'count', 'court_number': 'label'})
            courts.to_dict(orient='records')
            # TODO: terminar de arrumar essa parte
            data.append(complete_df_to_dict(courts, day, 'tennis', 1))
            print(data)
        tennis_data = sum(data, [])
        return render(request, 'activity_calendar.html',
                      {'activity_name': activity, 'activity_slots': json.dumps(tennis_data)})
    return render(request, 'calendar.html')


def code_generator(n):
    return [uuid.uuid1() for _ in range(n)]


@login_required
def user_dashboard(request):
    options = [{'name': 'Gym', 'icon': 'fitness_center', 'color': '#FFC107'},
               {'name': 'Parking', 'icon': 'garage', 'color': '#FFC107'},
               {'name': 'Tennis', 'icon': 'sports_tennis', 'color': '#FFC107'},
               {'name': 'Party', 'icon': 'celebration', 'color': '#FFC107'},
               {'name': 'Visitors', 'icon': 'groups', 'color': '#FFC107'},
               {'name': 'Setting', 'icon': 'manage_accounts', 'color': '#FFC107'}]
    return render(request, 'user_dashboard.html', {'options': options})


def gym_session_calendar(request):
    calendar = schedule()
    return render(request, 'calendar.html',
                  {'activity_name': activity, 'elements': [1, 2, 3, 4, 5, 6], 'calendar': calendar})


@login_required
def activity_calendar(request):
    return render(request, 'activity_calendar.html',
                  {'activity_name': activity, 'elements': [1, 2, 3, 4, 5, 6], 'calendar': calendar})


@login_required
def add_booking(request):
    dt_str = request.POST['timeStamp']  # datetime string
    dt = datetime.strptime(dt_str, "%m/%d/%Y, %H:%M").replace(tzinfo=timezone.utc)
    user = MyUser.objects.get(email=request.user)
    count_ts = GymSession.objects.filter(session_datetime=dt).count()  # Number of Training Sessions same Time
    # User can't book more than one session at the same day
    cur_day = datetime.strptime(dt_str, "%m/%d/%Y, %H:%M").replace(hour=0, minute=0, second=0, microsecond=0,
                                                                   tzinfo=timezone.utc)
    after_day = cur_day + timedelta(days=1)
    user_ct = GymSession.objects.filter(session_datetime__gte=cur_day, session_datetime__lt=after_day,
                                        booked_user=user).count()
    if count_ts < 4 and user_ct < 1:  # TODO: insert based on the condo
        GymSession.objects.create(session_datetime=dt, booked_user=user)
        return render(request, 'calendar.html', context={'calendar': schedule()})
    else:
        return render(request, 'calendar.html', context={'calendar': schedule()})


@login_required
def add_booking_activity(request, activity):
    if request.method == 'POST':
        user = MyUser.objects.get(email=request.user)
        activity_id = request.POST['activityId']
        date = datetime.strptime(request.POST['timeStamp'], "%m/%d/%Y, %H:%M")
        if activity == 'parking':
            stall = Stall.objects.get(id=activity_id)
            StallReservation.objects.create(user=user, stall=stall, date=date.date())
            print(activity_id, date, user, activity)
            print(request.POST)
            return render(request, 'activity_calendar.html', {'activity_name': activity})
        elif activity == 'party':
            party_room = PartyRoom.objects.get(id=activity_id)
            print(activity_id, date, user)
            print(party_room)
            PartyRoomReservation.objects.create(user=user, party_room=party_room, day_of_use=date.date())
            print(activity)
            print(request.POST)
            return render(request, 'activity_calendar.html', {'activity_name': activity})
        elif activity == 'tennis':

            pass
    else:
        return redirect('user_dashboard')


@login_required
def delete_booking(request):
    ts_id = request.POST['id']  # training session booking id
    GymSession.objects.filter(id=ts_id).delete()
    return render(request, 'calendar_dashboard.html', context={'user_schedule': user_schedule(request)})


@login_required
def delete_booking_activity(request, activity):
    if request.method == 'POST':
        id = request.POST['id']
        if activity == 'parking':
            pass
        elif activity == 'party':
            pass
        elif activity == 'tennis':
            pass
    ts_id = request.POST['id']  # training session booking id
    GymSession.objects.filter(id=ts_id).delete()
    return render(request, 'calendar_dashboard.html', context={'user_schedule': user_schedule(request)})


@login_required  # TODO: change for staff
def generate_codes(request):
    user = MyUser.objects.get(email=request.user)
    # if request.method == 'POST' and user.is_staff: #TODO: para quando for staff
    if request.method == 'POST' and user.is_staff:
        codes = code_generator(int(request.POST['quantity']))
        n_codes = GenerateCodeForm(request.POST)
        print(str(codes))  # TODO: send remove
        condo = Condo.objects.filter(condo=user.condo)
        for code in codes:
            SignupCode.objects.create(code=code, condo_id=condo)
        return render(request, 'code_generator.html', context={'codes': codes})
    else:
        return render(request, 'code_generator.html')


@login_required
#  making one temporal view request for coding user dashboard
def calendar(request):
    return render(request, 'calendar.html')
