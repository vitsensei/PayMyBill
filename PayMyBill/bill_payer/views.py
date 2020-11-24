from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Company, Payment
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone


def index(request):
    return render(request, r"bill_payer/index.html", {"navbar": loader.get_template(r"bill_payer/navbar.html"),
                                                      "yield": loader.get_template(r"bill_payer/signup.html")})


def signup(request):
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
        return HttpResponseNotFound('<h1>Page not found</h1>')


def payments(request, company_name):
    try:
        company = Company.objects.get(name=company_name)

    except Company.DoesNotExist:
        raise Http404(f"Company {company_name} does not exist.")

    else:
        return HttpResponse(reverse("bill_payer:index"))


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

