# Generated by Django 4.0.2 on 2022-04-11 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_myuser_first_name_myuser_gender_myuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Not Applicable')], max_length=1),
        ),
        migrations.AlterField(
            model_name='tenniscourtreservation',
            name='date',
            field=models.DateField(),
        ),
    ]
