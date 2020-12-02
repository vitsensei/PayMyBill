from random import randint

from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase

from .models import *
from .views import *


list_of_company_name = [
    "SP3D",
    "BAE Systems",
    "Floyd",
    "3DPC",
    "Austal",
    "Rowlands",
    "Boeing"
]

list_of_destination = [
    "https://www.google.com/",
    "https://www.python.org/",
    "https://www.djangoproject.com/",
    "https://www.django-rest-framework.org/",
    "https://numpy.org/",
    "https://www.scipy.org/"
]


class PaymentUnitTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(email="user1@random.com",
                                                   password="pass")

        c = Company.objects.create(user=self.user,
                               name="AML3D",
                               bsb=123456,
                               account_num=654321)

        self.all_payment_url = 'http://localhost:8000/bill_payer/resources/payment'

    def test_create_payment(self):
        global list_of_company_name

        payment = {
            "name": list_of_company_name[randint(0, len(list_of_company_name) - 1)],
            "bsb": str(randint(100000, 999999)),
            "account_num": str(randint(100000, 999999)),
            "amount": str(randint(0, 10000)),
            "status": "0"
        }

        request = self.factory.post(self.all_payment_url, data=payment)
        force_authenticate(request, user=self.user)

        view = PaymentList.as_view()
        response = view(request)
        response.render()

        assert response.status_code == 201, f"Actual response: {response.status_code}"

    def test_get_payment(self):
        self.test_create_payment()

        payment = Payment.objects.all().first()
        request = self.factory.get(self.all_payment_url + f"//{payment.id}")
        force_authenticate(request, user=self.user)

        view = PaymentDetail.as_view()
        response = view(request, pk=str(payment.id))
        response.render()

        assert response.status_code == 200, f"Actual response: {response.status_code}"

    def test_get_all_payment(self):
        self.test_create_payment()
        self.test_create_payment()
        self.test_create_payment()

        request = self.factory.get(self.all_payment_url)
        force_authenticate(request, user=self.user)

        view = PaymentList.as_view()
        response = view(request)
        response.render()

        assert response.status_code == 200, f"Actual response: {response.status_code}"

    def test_modify_payment(self):
        self.test_create_payment()

        payment = Payment.objects.all().first()

        updated_data = {
            "name": payment.name,
            "bsb": payment.bsb,
            "account_num": payment.account_num,
            "amount": payment.amount,
            "status": 1
        }

        request = self.factory.post(self.all_payment_url + f"//{payment.id}", data=updated_data)
        force_authenticate(request, user=self.user)

        view = PaymentDetail.as_view()
        response = view(request, pk=str(payment.id))
        response.render()

        assert response.status_code == 201, f"Actual response: {response.status_code}"

    def test_delete_payment(self):
        self.test_create_payment()

        payment = Payment.objects.all().first()

        request = self.factory.delete(self.all_payment_url + f"//{payment.id}")
        force_authenticate(request, user=self.user)

        view = PaymentDetail.as_view()
        response = view(request, pk=str(payment.id))
        response.render()

        assert response.status_code == 204, f"Actual response: {response.status_code}"


class HookUnitTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(email="user2@random.com",
                                                   password="pass")

        c = Company.objects.create(user=self.user,
                               name="AML3D",
                               bsb=987654,
                               account_num=456789)

        self.all_hook_url = 'http://localhost:8000/bill_payer/resources/hook'

    def test_create_hook(self):
        global list_of_destination

        url = list_of_destination[randint(0, len(list_of_destination) - 1)]
        hook = {
            "url": list_of_destination[randint(0, len(list_of_destination) - 1)]
        }

        request = self.factory.post(self.all_hook_url, data=hook)
        force_authenticate(request, user=self.user)

        view = HookList.as_view()
        response = view(request)
        response.render()

        assert response.status_code == 201, f"Actual response: {response.status_code}"

    def test_get_all_hook(self):
        self.test_create_hook()
        self.test_create_hook()
        self.test_create_hook()

        request = self.factory.get(self.all_hook_url)
        force_authenticate(request, user=self.user)

        view = HookList.as_view()
        response = view(request)
        response.render()

        assert response.status_code == 200, f"Actual response: {response.status_code}"

    def test_get_hook(self):
        pass

    def test_modify_hook(self):
        pass

    def test_delete_hook(self):
        pass

