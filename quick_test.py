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

company_url = 'http://localhost:8000/bill_payer/resources/company'
all_payment_url = 'http://localhost:8000/bill_payer/resources/payment'
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


def get_all_payment(token):
    global all_payment_url

    r = requests.get(all_payment_url, headers=create_header(token))

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
    payment["status"] = 1
    r = requests.post(single_payment_url, headers=create_header(token), data=payment)

    return r.json()


# Get token
token = get_token("user1@random.com", "pass")

# Test getting all payments in this account
# payments = get_all_payment(token)
# pprint(payments)

# Test getting one payment in this account
# payment = get_single_payment(token, 3)
# pprint(payment)

# Test creating a new payment
# post_random_payment(token)

# Testing updating an existing payment
payment = update_existing_payment(token, 3)
pprint(payment)