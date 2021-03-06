# Generated by Django 3.1.3 on 2020-11-30 01:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill_payer', '0002_auto_20201128_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_date',
            field=models.DateTimeField(default=datetime.datetime(2120, 11, 6, 1, 6, 32, 997021), verbose_name='paid date'),
        ),
        migrations.CreateModel(
            name='Hook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=200)),
                ('is_subscribed_name', models.BooleanField(default=False)),
                ('is_subscribed_bsb', models.BooleanField(default=False)),
                ('is_subscribed_account_num', models.BooleanField(default=False)),
                ('is_subscribed_amount', models.BooleanField(default=False)),
                ('is_subscribed_status', models.BooleanField(default=False)),
                ('company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hook', to='bill_payer.company')),
            ],
        ),
    ]
