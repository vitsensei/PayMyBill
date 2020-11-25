from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Company, Payment
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone


def index(request):
    return render(request, r"bill_payer/index.html", {"navbar": loader.get_template(r"bill_payer/navbar.html"),
                                                      "yield": loader.get_template(r"bill_payer/home.html")})


def signup(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            email = request.POST["email"]
            password = request.POST["password"]
            bsb = request.POST["bsb"]
            account_num = request.POST["account_num"]

            company = Company(name=name,
                              email=email,
                              password=password,
                              bsb=int(bsb),
                              account_num=int(account_num),
                              signup_date=timezone.now())

            return HttpResponseRedirect(reverse('bill_payer:payments', args=(company.name,)))

        except:
            return HttpResponseNotFound("Fail to register new company.")

    else:
        return render(request, r"bill_payer/index.html", {"navbar": loader.get_template(r"bill_payer/navbar.html"),
                                                          "yield": loader.get_template(r"bill_payer/signup.html")})


def signin(request):
    try:
        email = request.POST["email"]
        password = request.POST["password"]

        company = Company.objects.get(email=email,
                                      password=password)

        return HttpResponseRedirect(reverse('bill_payer:payments', args=(company.name,)))

    except Company.DoesNotExist:
        return HttpResponseNotFound("Fail to login.")


def payments(request, company_name):
    try:
        company = Company.objects.get(name=company_name)

    except Company.DoesNotExist:
        raise Http404(f"Company {company_name} does not exist.")

    else:
        return render(request, "bill_payer/payments.html", {"list_of_payments": company.payment_set.all})


def details(request, company_name, payment_id):
    try:
        company = Company.objects.get(name=company_name)

    except Company.DoesNotExist:
        raise Http404(f"Company {company_name} does not exist.")

    else:
        try:
            payment = Company.payment_set.get(name=payment_id)

        except Payment.DoesNotExist:
            raise Http404(f"Payment {payment_id} of company {company_name} does not exist.")

        else:
            return HttpResponse(f"Details of one payment with id {payment_id} of company {company_name}")

