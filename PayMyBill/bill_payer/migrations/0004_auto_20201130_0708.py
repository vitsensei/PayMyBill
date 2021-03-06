# Generated by Django 3.1.3 on 2020-11-30 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_payer', '0003_auto_20201130_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hook',
            name='is_subscribed_account_num',
        ),
        migrations.RemoveField(
            model_name='hook',
            name='is_subscribed_amount',
        ),
        migrations.RemoveField(
            model_name='hook',
            name='is_subscribed_bsb',
        ),
        migrations.RemoveField(
            model_name='hook',
            name='is_subscribed_name',
        ),
        migrations.RemoveField(
            model_name='hook',
            name='is_subscribed_status',
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_date',
            field=models.DateTimeField(default=datetime.datetime(2120, 11, 6, 7, 8, 52, 502892), verbose_name='paid date'),
        ),
    ]
