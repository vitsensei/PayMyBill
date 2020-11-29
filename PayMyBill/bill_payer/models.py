from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


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

    def __str__(self):
        return f"{self.company.name} to {self.name} (${self.amount})"

