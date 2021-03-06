# Generated by Django 4.0.2 on 2022-03-29 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('date_of_birth', models.DateField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=11)),
                ('user_type', models.CharField(choices=[('RU', 'Resident User'), ('CA', 'Condo Admin'), ('SP', 'Service Provider')], default='RU', max_length=2)),
                ('user_status', models.CharField(choices=[('A', 'Active'), ('P', 'Penalized'), ('I', 'Inactive')], default='A', max_length=1)),
                ('address', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Condo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartyRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=16)),
                ('condo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.condo')),
            ],
        ),
        migrations.CreateModel(
            name='Stall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stall_label', models.CharField(max_length=8)),
                ('stall_type', models.CharField(choices=[('V', 'VISITOR'), ('R', 'RESIDENT')], default='V', max_length=1)),
                ('condo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.condo')),
            ],
        ),
        migrations.CreateModel(
            name='TennisCourt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_number', models.IntegerField()),
                ('time_slot', models.TimeField()),
                ('condo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.condo')),
            ],
        ),
        migrations.CreateModel(
            name='TennisCourtReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_time', models.DateTimeField()),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.tenniscourt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StallReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('stall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.stall')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SignupCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=36)),
                ('use_status', models.CharField(choices=[('U', 'Used'), ('A', 'Available')], default='A', max_length=1)),
                ('condo_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.condo')),
            ],
        ),
        migrations.CreateModel(
            name='Penalties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty_amount', models.IntegerField()),
                ('penalty_reason', models.CharField(max_length=100)),
                ('penalty_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartyRoomReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_use', models.DateField()),
                ('party_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.partyroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GymSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_code', models.CharField(default='00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', max_length=128)),
                ('session_datetime', models.DateTimeField()),
                ('booking_status', models.CharField(choices=[('B', 'Booked'), ('C', 'Canceled'), ('M', 'Missed')], default='B', max_length=1)),
                ('booked_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='condo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.condo'),
        ),
    ]
