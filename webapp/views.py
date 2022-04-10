from datetime import datetime, timezone, date, timedelta, time
from itertools import chain
import json
import pandas as pd
import uuid

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
from .admin import UserCreationForm
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect

from webapp.forms import *
from webapp.models import *
from webapp.admin import *
from webapp.constants import *



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
    if not df.empty:
        df['hour'] = df[col].apply(lambda s: s.hour)
        df['minute'] = df[col].apply(lambda s: s.minute)
        df['time'] = df[col].apply(lambda s: time(hour=s.hour, minute=s.minute))
    return df


def split_datetime(df, col, has_time=False):
    if has_time:
        df = split_time(df, col)

    df['day'] = df[col].apply(lambda s: s.day)
    df['month'] = df[col].apply(lambda s: s.month)
    df['year'] = df[col].apply(lambda s: s.year)

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


def user_activity_schedule(request, activity_type):
    user = MyUser.objects.get(email='admin@gmail.com')
    has_time = False
    if activity_type == 'parking':
        query = StallReservation.objects.filter(user=user)
    elif activity_type == 'gym':
        query = GymSession.objects.filter(user=user)
    elif activity_type == 'party':
        query = PartyRoomReservation.objects.filter(user=user)
    elif activity_type == 'tennis':
        query = TennisCourtReservation.objects.filter(user=user)
        has_time = True
    else:
        return None

    if query.exists():
        df = pd.DataFrame(list(query.values()))
        df = split_datetime(df, 'date', has_time)
        if not has_time:
            df['hour'], df['minute'] = 0, 0      #TODO: walk around
        df['type'] = activity_type
        return json.dumps(df.to_dict(orient='records'), default=str)
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


def prepare_activity_schedule(cur_date, activityRooms, activityReservationQuery, type, activity_id, label_name, qtlimit,
                              group):
    data = []
    for day in [cur_date + timedelta(days=x) for x in range(7)]:
        rooms = pd.DataFrame(list(activityRooms.values()))
        reservations = activityReservationQuery.filter(date__gte=day, date__lt=day + timedelta(1)).values()

        if not reservations.exists():
            reservations = pd.DataFrame({activity_id: [], 'user_id': []})
        else:
            reservations = pd.DataFrame(list(reservations))
        if type == 'tennis':
            reservations['hour'], reservations['minute'] = reservations['date'].dt.hour, reservations['date'].dt.minute
        rooms = rooms.merge(reservations, left_on='id', right_on=activity_id, how='left', suffixes=('', '_y')).groupby(
            group).count()['user_id'].reset_index().rename(columns={'user_id': 'count', label_name: 'label'})
        rooms['day'] = day.day
        rooms['month'] = day.month
        rooms['year'] = day.year
        if not type == 'tennis':
            rooms['hour'], rooms['minute'] = 0, 0
        rooms['type'] = type
        rooms['qtlimit'] = qtlimit  # depends on the activity
        data.append(rooms.to_dict(orient='records'))
    data = sum(data, [])

    return data


def reservation_exist(queryObj, col_dic):
    if not queryObj.exists():
        return pd.DataFrame(col_dic)
    else:
        return pd.DataFrame(list(queryObj))


def complete_df_to_dict(df, time, type, qtlimit):
    df['day'], df['month'], df['year'] = time.day, time.month, time.year
    df['type'], df['qtlimit'] = type, qtlimit
    if isinstance(time, datetime):
        df['hour'], df['minute'] = time.hour, time.minute
    else:
        df['hour'], df['minute'] = 0, 0
    return df.to_dict(orient='records')


def index(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
        return redirect('user_login')


def signup(request):
    if request.method == 'POST':
        code_form = CodeForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            code = SignupCode.objects.get(code=code_form)
            if code.exists():
                user = form.save()
                condo = Condo.objects.get(id=code.condo_id)
                user.condo = condo
                user.save() #TODO: ver c isso ta certo
                # TODO: tambem mudar o status do codigo usado

                # log the user in
                return redirect('index')
            else:
                #TODO: caso de erro codigo errado
                return render(request, "signup.html", {'form': form, 'code_form': code_form})
    else:
        form = UserCreationForm()
        code_form = CodeForm(request.POST)
    return render(request, "signup.html", {'form': form, 'code_form': code_form})


def condo_signup(request): #TODO: remover
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
            return render(request, "login.html", {'form': form, 'alert_msg': MESSAGES['error_password']})
            # return redirect('index')
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def admin_dashboard(request):
    return redirect('/admin/')


def code_generator(n):
    return [uuid.uuid1() for _ in range(n)]


@login_required
def user_dashboard(request):
    options = ACTIVITY_OPTIONS
    if not request.user.is_staff:
        options.remove('settings')
    return render(request, 'user_dashboard.html', {'options': options})


@login_required
def gym_session_calendar(request):
    calendar = schedule()
    return render(request, 'calendar.html',
                  {'activity_name': 'gym', 'elements': [1, 2, 3, 4, 5, 6], 'calendar': calendar})


@login_required
def activity_dashboard(request, activity_type):
    if activity_type == 'gym':
        return render(request, 'calendar_dashboard.html', context={'user_schedule': user_schedule(request)})
    if activity_type == 'settings':
        pass
    else:
        return render(request, 'activity_dashboard.html',
                      context={'activity_type': activity_type, 'activity_labels': ACTIVITIES_DASH[activity_type], 'user_activity_schedule': user_activity_schedule(request, activity_type)})


@login_required
def activity_calendar(request, activity_type):
    today = datetime.today()
    cur_date = datetime(day=today.day, month=today.month, year=today.year) - timedelta(1)
    date_ahead = cur_date + timedelta(7)  # TODO mudar aqui pra pegar a do dia e quando o usuario pedir
    user = MyUser.objects.get(email=request.user)
    data = []
    if activity_type == 'gym':
        return render(request, 'calendar_dashboard.html', {'user_schedule': user_schedule(request)})
    elif activity_type == 'parking':
        stalls_query = Stall.objects.filter(condo=user.condo)
        reservations_query = StallReservation.objects.filter(date__gte=cur_date, date__lte=date_ahead)
        data = prepare_activity_schedule(cur_date, stalls_query, reservations_query, 'parking', 'stall_id',
                                         'stall_label', 1, ['id', 'stall_label'])
    elif activity_type == 'party':
        party_query = PartyRoom.objects.filter(condo=user.condo)
        reservations_query = PartyRoomReservation.objects.filter(date__gte=cur_date, date__lte=date_ahead)
        data = prepare_activity_schedule(cur_date, party_query, reservations_query, 'party', 'party_room_id',
                                         'room_name', 1, ['id', 'room_name'])
    elif activity_type == 'tennis':
        # TODO: aqui tenho que verificar se o merge das chaves esta correto e se isso ta certo  no uml
        for day in [cur_date + timedelta(days=x) for x in range(7)]:
            courts = pd.DataFrame(list(TennisCourt.objects.filter(condo=user.condo).values()))
            reservations = TennisCourtReservation.objects.filter(date__gte=day,
                                                                 date__lte=day + timedelta(1)).values()
            reservations = reservation_exist(reservations, {'court_id': [], 'user_id': [], 'hour': [], 'minute': []})
            reservations = split_time(reservations, 'date')
            print(reservations)
            print(courts)
            courts = split_time(courts, 'time_slot')
            courts = \
                courts.merge(reservations, left_on=['id'], right_on=['court_id'],
                             how='left', suffixes=('', '_y')).groupby(
                    ['id', 'court_number', 'hour', 'minute']).count()['user_id'].reset_index().rename(
                    columns={'user_id': 'count', 'court_number': 'label'})
            print("after merge")
            print(courts)
            courts.to_dict(orient='records')
            data.append(complete_df_to_dict(courts, day, 'tennis', 1))
        data = sum(data, [])

    return render(request, 'activity_calendar.html',
                  {'activity_name': activity_type, 'activity_slots': json.dumps(data)})


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
            print(activity_id, date.date(), user, activity) #TODO: remove
            print(request.POST)#TODO: remove

        elif activity == 'party':
            party_room = PartyRoom.objects.get(id=activity_id)
            print(activity_id, date, user)#TODO: remove
            print(party_room)#TODO: remove
            PartyRoomReservation.objects.create(user=user, party_room=party_room, date=date.date())
            print(request.POST)#TODO: remove
        elif activity == 'tennis':
            tennis_court = TennisCourt.objects.get(id=activity_id)
            print(activity_id, date, user)#TODO: remove
            print(tennis_court)#TODO: remove
            TennisCourtReservation.objects.create(user=user, court=tennis_court, date=date.date())
            print(request.POST)#TODO: remove
            pass
        elif activity == 'gym':
            pass # todo tem que fazer aqui
        return redirect('activity_calendar', activity_type=activity)
    else:
        return redirect('user_dashboard')


@login_required
def delete_booking(request):
    ts_id = request.POST['id']  # training session booking id
    GymSession.objects.filter(id=ts_id).delete()
    return render(request, 'calendar_dashboard.html', context={'user_schedule': user_schedule(request)})


@login_required
def delete_activity_reservation(request, activity_type):
    if request.method == 'POST':
        id = request.POST['id']
        if activity_type == 'parking':
            StallReservation.objects.filter(id=id).delete()
        elif activity_type == 'party':
            PartyRoomReservation.objects.filter(id=id).delete()
        elif activity_type == 'tennis':
            TennisCourtReservation.objects.filter(id=id).delete()
        elif activity_type == 'gym':
            GymSession.objects.filter(id=id).delete()

    return redirect('activity_dashboard', activity_type=activity_type)


@staff_member_required
def generate_codes(request):
    user = MyUser.objects.get(email=request.user)
    print(user)
    if request.method == 'POST':
        val_int = int(request.POST['quantity'])
        if val_int > 0:
            codes = code_generator(val_int)
            n_codes = GenerateCodeForm(request.POST)
            print(str(codes))  # TODO: send remove
            condo = Condo.objects.get(id=user.condo_id)
            # for code in codes: # TODO:klimpar aqui depois
            #     SignupCode.objects.create(code=code, condo_id=condo)
            print(condo)
            return render(request, 'code_generator.html', context={'codes': codes})
        else:
            #TODO: send error message
            return render(request, 'code_generator.html')
    else:
        return render(request, 'code_generator.html')
