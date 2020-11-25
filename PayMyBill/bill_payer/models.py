from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    bsb = models.CharField(max_length=200)
    account_num = models.CharField(max_length=200)
    signup_date = models.DateTimeField('publish date')

    def __str__(self):
        return self.name


class Payment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    amount = models.FloatField(default=0)

    name = models.CharField(max_length=200)
    bsb = models.CharField(max_length=200)
    account = models.CharField(max_length=200)

    create_date = models.DateTimeField('publish date')

    status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.company.name} to {self.name} (${self.amount})"

