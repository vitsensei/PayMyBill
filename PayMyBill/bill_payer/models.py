from django.db import models
from django.utils import timezone


class Company(models.Model):
    # Name of the company
    name = models.CharField(max_length=200)

    # Email and password, used for login
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    # Account's info
    bsb = models.CharField(max_length=200)
    account_num = models.CharField(max_length=200)

    # The date this company is created
    signup_date = models.DateTimeField('created date', auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    # The company that owns this payment
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Amount of money
    amount = models.FloatField(default=0)

    # The receiver's info
    name = models.CharField(max_length=200)
    bsb = models.CharField(max_length=200)
    account_num = models.CharField(max_length=200)

    # The date this payment is created
    created_date = models.DateTimeField('created date', auto_now_add=True)

    # The date this payment is paid
    paid_date = models.DateTimeField('paid date', auto_now=True)

    """
    status indicate the following 4 states:
    0 - created
    1 - successful
    2 - failed
    3 - disputed
    """
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.company.name} to {self.name} (${self.amount})"

