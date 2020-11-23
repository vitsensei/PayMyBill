from django.http import HttpResponse


def index(request):
    return HttpResponse("Page to sign in/sign up.")


def payments(request, company_name):
    return HttpResponse(f"Page to mange all the payments of company {company_name}")


def details(request, company_name, payment_id):
    return HttpResponse(f"Details of one payment with id {payment_id} of company {company_name}")

