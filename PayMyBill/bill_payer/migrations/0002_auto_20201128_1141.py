# Generated by Django 3.1.3 on 2020-11-28 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill_payer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
