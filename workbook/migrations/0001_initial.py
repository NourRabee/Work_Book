# Generated by Django 5.1 on 2024-09-08 17:52

import django.db.models.deletion
import django.utils.timezone
import workbook.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=300)),
                ('salt', models.CharField(max_length=29)),
                ('profile_picture', models.TextField(blank=True, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('role', models.CharField(choices=[('CUSTOMER', 'CUSTOMER'), ('WORKER', 'WORKER')], default=workbook.enums.UserType['CUSTOMER'], max_length=29)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_time', models.IntegerField(blank=True, null=True)),
                ('time_slot_period', models.IntegerField(blank=True, help_text='Duration of the time slot in seconds', null=True)),
                ('group_id', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('CONFIRMED', 'CONFIRMED'), ('REJECTED', 'REJECTED'), ('IN PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED')], default=workbook.enums.ReservationStatus['IN_PROGRESS'], max_length=29)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('description', models.TextField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=300, unique=True)),
                ('token_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.user')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workbook.user'),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('day_start_time', models.IntegerField(blank=True, help_text='Duration of the time slot in seconds', null=True)),
                ('day_end_time', models.IntegerField(blank=True, help_text='Duration of the time slot in seconds', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workbook.user')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('flag', models.CharField(choices=[('CUSTOMER', 'CUSTOMER'), ('WORKER', 'WORKER')], default=workbook.enums.MessageSender['CUSTOMER'], max_length=29)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.customer')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.worker')),
            ],
        ),
        migrations.CreateModel(
            name='WorkerSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot_period', models.IntegerField(help_text='Duration of the time slot in seconds')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.skill')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.worker')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='worker_skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook.workerskill'),
        ),
        migrations.AddConstraint(
            model_name='workerskill',
            constraint=models.UniqueConstraint(fields=('worker', 'skill'), name='unique_worker_skill'),
        ),
    ]
