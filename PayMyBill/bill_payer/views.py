from django.http import HttpResponse, Http404
from .models import Company, Payment


def index(request):
    return HttpResponse("Page to sign in/sign up.")


def payments(request, company_name):
    try:
        company = Company.objects.get(name=company_name)

    except Company.DoesNotExist:
        raise Http404(f"Company {company_name} does not exist.")

    else:
        return HttpResponse(f"Page to mange all the payments of company {company_name}")


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

