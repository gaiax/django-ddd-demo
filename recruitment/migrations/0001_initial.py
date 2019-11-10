# Generated by Django 2.2.7 on 2019-11-10 09:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecruiterRDB',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ScreeningRDB',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('apply_date', models.DateField()),
                ('status', models.SmallIntegerField()),
                ('applicant_email_address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='InterviewRDB',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('interview_date', models.DateField()),
                ('interview_number', models.IntegerField()),
                ('screening_step_result', models.SmallIntegerField()),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.RecruiterRDB')),
                ('screening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.ScreeningRDB')),
            ],
        ),
    ]
