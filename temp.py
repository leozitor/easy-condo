import json
import pandas as pd
from datetime import datetime, timedelta, date
from itertools import chain

from django.db.models import Q


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
    df['training_datetime'] = pd.to_datetime(df['training_datetime'])

    df['year'] = df['training_datetime'].dt.year
    df['month'] = df['training_datetime'].dt.month
    df['day'] = df['training_datetime'].dt.day
    df['hour'] = df['training_datetime'].dt.hour
    df['minute'] = df['training_datetime'].dt.minute

#
# def user_schedule(request):
#     practitioner = Practitioner.objects.get(user=request.user)
#     query = TrainingSession.objects.filter(booked_user=practitioner)
#     if query.exists():
#         df = pd.DataFrame(list(query.values()))
#         add_pd_datetime(df)
#         df = df[['id', 'hour', 'minute', 'day', 'month', 'year']]
#         return json.dumps(df.to_dict(orient='records'))
#     else:
#         return None

#
# def query_schedule():
#     dt = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
#     query = TrainingSession.objects.filter(training_datetime__gte=dt)
#     if query.exists():
#         df = pd.DataFrame(list(query.values()))
#         add_pd_datetime(df)
#         return df
#     else:
#         return None


Stall.objects.raw('SELECT * FROM myapp_person')

s = StallReservation.objects.select_related('stall').filter(Q(checkin__lte=cur_date, checkout__gte=cur_date)|Q(stall=True))

stalls = Stall.objects.filter(condo=1)
stalls = pd.DataFrame(list(stalls.values()))

sr = StallReservation.objects.filter(checkin__lte=cur_date, checkout__gte=cur_date)
sr = pd.DataFrame(list(sr.values()))

sr['date']=sr.apply(lambda x : pd.date_range(start=x['checkin'], end=x['checkout'], freq='MS') ,axis=1)
sr=sr.explode('date')
df.EndDate=df.StartDate+pd.tseries.offsets.MonthEnd()