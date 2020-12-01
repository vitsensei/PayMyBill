from pprint import pprint
from random import randint
from datetime import datetime, timedelta

import requests


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

company_url = 'http://localhost:8000/bill_payer/resources/company'
all_payment_url = 'http://localhost:8000/bill_payer/resources/payment'
all_hook_url = 'http://localhost:8000/bill_payer/resources/hook'
token_url = 'http://localhost:8000/bill_payer/token'


def create_header(token):
    return {"Authorization": "Token " + token}


def generate_random_payment():
    global list_of_company_name

    payment = {
        "name": list_of_company_name[randint(0, len(list_of_company_name) - 1)],
        "bsb": str(randint(100000, 999999)),
        "account_num": str(randint(100000, 999999)),
        "amount": str(randint(0, 10000)),
        "created_date": str(datetime.now()),
        "paid_date": str(datetime.now() + timedelta(days=36500)),
        "status": "0"
    }

    return payment


def get_token(id, password):
    global token_url

    # Get TOKEN
    acc = {
        "username": str(id),
        "password": str(password)
    }

    r = requests.request("POST", token_url, data=acc)

    token = r.json()["token"]

    return token


def get_all(token, address):
    r = requests.get(address, headers=create_header(token))
    return r.json()


def get_all_payment(token):
    global all_payment_url

    r = get_all(token, all_payment_url)

    return r.json()


def get_single_payment(token, payment_id):
    global all_payment_url
    single_payment_url = all_payment_url + f"/{payment_id}"

    r = requests.get(single_payment_url, headers=create_header(token))
    return r.json()


def post_random_payment(token):
    global all_payment_url

    requests.post(all_payment_url, headers=create_header(token), data=generate_random_payment())


def update_existing_payment(token, payment_id):
    global all_payment_url
    single_payment_url = all_payment_url + f"/{payment_id}"

    payment = get_single_payment(token, payment_id)
    payment["status"] = 0
    r = requests.post(single_payment_url, headers=create_header(token), data=payment)

    return r.json()


def delete_payment(token, payment_id):
    global all_payment_url
    single_payment_url = all_payment_url + f"/{payment_id}"

    requests.delete(single_payment_url, headers=create_header(token))


def get_all_hook(token):
    global all_hook_url

    r = get_all(token, all_hook_url)

    return r.json()


def get_existing_hook(token, hook_id):
    global all_hook_url
    single_hook_url = all_hook_url + f"/{hook_id}"

    r = requests.get(single_hook_url, headers=create_header(token))
    return r.json()


def generate_random_hook():
    global list_of_destination

    url = list_of_destination[randint(0, len(list_of_destination) - 1)]
    hook = {
        "url": list_of_destination[randint(0, len(list_of_destination) - 1)],
        "is_subscribed_name": str(int(randint(0, 100) % 2 == 1)),
        "is_subscribed_bsb": str(int(randint(0, 100) % 2 == 1)),
        "is_subscribed_account_num": str(int(randint(0, 100) % 2 == 1)),
        "is_subscribed_amount": str(int(randint(0, 100) % 2 == 1)),
        "is_subscribed_status": str(int(randint(0, 100) % 2 == 1))
    }

    return hook


def post_random_hook(token):
    global all_hook_url

    requests.post(all_hook_url, headers=create_header(token), data=generate_random_hook())

# Get token
token = get_token("user2@random.com", "pass")

################ Test Payment ################
#### GET ####
# Test getting all payments in this account
# payments = get_all_payment(token)
# pprint(payments)

# Test getting one payment in this account
# payment = get_single_payment(token, 3)
# pprint(payment)

#### POST ####
# Test creating a new payment
# post_random_payment(token)

# Test updating an existing payment
# payment = update_existing_payment(token, 3)
# pprint(payment)

#### DELETE ####
# delete_payment(token, 2)

################ Test Hook ################
# Test get all hooks
# hooks = get_all_hook(token)
# pprint(hooks)

# Test get a specific hook
# hook = get_existing_hook(token, hook_id=1)
# pprint(hook)

# Test post a random hook
# post_random_hook(token)