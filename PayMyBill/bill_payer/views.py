from django.http import HttpResponse


def index(request):
    return HttpResponse("Page to sign in/sign up.")


def payments(request):
    return HttpResponse("Page to mange all the payments")


def details(request):
    return HttpResponse("Details of one payment")