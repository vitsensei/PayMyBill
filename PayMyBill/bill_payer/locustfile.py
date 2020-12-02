from random import randint

from locust import HttpUser, task


class LoadTest(HttpUser):
    auth = None
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header = None

    def post_new_payment(self):
        data = {
            "name": self.list_of_company_name[randint(0, len(self.list_of_company_name) - 1)],
            "bsb": str(randint(100000, 999999)),
            "account_num": str(randint(100000, 999999)),
            "amount": str(randint(0, 10000)),
            "status": "0"
        }

        r = self.client.post(url='bill_payer/resources/payment',
                             headers=self.header,
                             json=data)

        return r

    def post_exist_payment(self):
        data = {
            "name": self.list_of_company_name[randint(0, len(self.list_of_company_name) - 1)],
            "bsb": str(randint(100000, 999999)),
            "account_num": str(randint(100000, 999999)),
            "amount": str(randint(0, 10000)),
            "status": str(randint(0, 4))
        }

        r = self.client.post(url='bill_payer/resources/payment/4',
                             headers=self.header,
                             json=data)

        return r

    def get_all_payment(self):
        r = self.client.get(url='bill_payer/resources/payment',
                            headers=self.header)

        return r

    def get_single_payment(self):
        r = self.client.get(url='bill_payer/resources/payment/4',
                            headers=self.header)

        return r

    @task
    def run_task(self):
        data = {
            "username": "user1@random.com",
            "password": "pass"
        }
        r = self.client.post("bill_payer/token",
                             json=data)

        token = r.json()["token"]

        self.header = {
            "Authorization": "Token " + str(token)
        }

        self.post_exist_payment()
        self.get_all_payment()
        self.get_single_payment()
