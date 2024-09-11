# Generated by Django 5.1 on 2024-09-05 08:23

import workbook.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0007_alter_reservation_time_slot_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='flag',
            field=models.CharField(choices=[('CUSTOMER', 'CUSTOMER'), ('WORKER', 'WORKER')], default=workbook.enums.MessageSender['CUSTOMER'], max_length=29),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('CONFIRMED', 'CONFIRMED'), ('REJECTED', 'REJECTED'), ('IN PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED')], default=workbook.enums.ReservationStatus['IN_PROGRESS'], max_length=29),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('CUSTOMER', 'CUSTOMER'), ('WORKER', 'WORKER')], default=workbook.enums.UserType['CUSTOMER'], max_length=29),
        ),
    ]
