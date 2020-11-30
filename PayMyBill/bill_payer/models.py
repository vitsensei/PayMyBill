from datetime import datetime, timedelta
from pprint import pprint

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import *
from django.dispatch import receiver
import requests


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        self._must(email, password)

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        self._must(email, password)

        user = self.create_user(
            email,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

    @staticmethod
    def _must(email, password):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an email address')


class CustomUser(AbstractBaseUser):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Empty for now...
    EMAIL_FIELD = "email"  # This is set by default, but just in case...

    @property
    def is_staff(self):
        return self.is_admin  # Staff == Admin

    def has_perm(self, perm, obj=None):
        # Not yet implemented
        print(f"asking for perm: {perm}")
        return True

    def has_module_perms(self, package_name):
        # Not yet implemented
        print(f"asking for module_perms: {package_name}")
        return True


class Company(models.Model):
    class Meta:
        verbose_name_plural = _("Companies")

    # The (custom) user model for auth
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="company")

    # Name of the company
    name = models.CharField(max_length=200)

    # Account's info
    bsb = models.CharField(max_length=200)
    account_num = models.CharField(max_length=200)

    # The date this company is created
    signup_date = models.DateTimeField('created date', auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    # The company that owns this payment
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="payment")

    # The receiver's info
    name = models.CharField(max_length=200)
    bsb = models.CharField(max_length=200)
    account_num = models.CharField(max_length=200)

    # Amount of money
    amount = models.FloatField(default=0)

    # The date this payment is created
    created_date = models.DateTimeField('created date', auto_now_add=True)

    # The date this payment is paid
    paid_date = models.DateTimeField('paid date', default=datetime.now() + timedelta(days=36500))

    """
    status indicate the following 4 states:
    0 - created
    1 - successful
    2 - failed
    3 - disputed
    """
    status = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        self.initial_state = {
            "name": self.name,
            "bsb": self.bsb,
            "account_num": self.account_num,
            "amount": self.amount,
            "status": self.status
        }

    def __str__(self):
        return f"{self.company.name} to {self.name} (${self.amount})"


class Hook(models.Model):
    # The web hook models allow each company to have multiple hook
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                default=1, related_name="hook")

    # The URL to make the POST request to
    url = models.CharField(max_length=200, default="")


def post_msg(msg, urls):
    pprint(msg)
    for url in urls:
        # requests.post(url, data=msg)
        print(f"Sending msg to {url}")


@receiver(post_save, sender=Payment)
def hook_update_handler(sender, **kwargs):
    instance = kwargs["instance"]
    created = kwargs["created"]

    c = instance.company
    urls = [hook.url for hook in c.hook.all()]

    if created:
        new_state = {
            "name": instance.name,
            "bsb": instance.bsb,
            "account_num": instance.account_num,
            "amount": instance.amount,
            "status": instance.status
        }

        hook_message = {
            "new_state": new_state,
            "msg": "New payment created"
        }

        post_msg(hook_message, urls)

    else:
        new_state = dict()
        previous_state = dict()
        msg = "State updated"

        for field_name in instance.initial_state.keys():
            current_state = getattr(instance, field_name)
            if current_state != instance.initial_state[field_name]:
                new_state[field_name] = current_state
                previous_state[field_name] = instance.initial_state[field_name]

        if len(new_state) > 0:
            hook_message = {
                "new_state": new_state,
                "previous_state": previous_state,
                "msg": "Payment updated"
            }

            post_msg(hook_message, urls)


@receiver(pre_delete, sender=Payment)
def hook_delete_handler(sender, **kwargs):
    instance = kwargs["instance"]

    c = instance.company
    urls = [hook.url for hook in c.hook.all()]

    hook_message = {
        "msg": f"Payment (id={instance.id}) is deleted."
    }

    post_msg(hook_message, urls)
