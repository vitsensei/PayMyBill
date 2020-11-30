from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader, Context, Template
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from .serializer import PaymentSerializer, CompanySerializer, HookSerializer
from .models import Company, Payment, Hook


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
        yield_template = loader.get_template('bill_payer/payments.html')

        return render(request, r"bill_payer/index.html", {"navbar": loader.get_template(r"bill_payer/navbar.html"),
                                                          "yield": yield_template,
                                                          "list_of_payments": company.payment_set.all()})


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


class CompanyDetail(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        if request.auth is None:
            response = HttpResponse
            response.status_code = 401

            return response()

        else:
            try:
                c = request.user.company
                serializer = CompanySerializer(c)

                return Response(serializer.data)

            except Company.DoesNotExist:
                error = {"Not found": {"The requested company is not found."}}
                return Response(error, status=status.HTTP_404_NOT_FOUND)


class PaymentList(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            c = request.user.company

            payments = c.payment.all()
            serializer = PaymentSerializer(payments, many=True)

            return Response(serializer.data)

        except Company.DoesNotExist:
            error = {"Not found": {"The requested company is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetail(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk, format=None):
        try:
            c = request.user.company

            payment = c.payment.get(pk=pk)
            serializer = PaymentSerializer(payment)

            return Response(serializer.data)

        except Company.DoesNotExist:
            error = {"Not found": {"The requested company is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        except Payment.DoesNotExist:
            error = {"Not found": {"The requested payment is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, format=None):
        try:
            c = request.user.company

            payment = c.payment.get(pk=pk)
            serializer = PaymentSerializer(payment, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        except Company.DoesNotExist:
            error = {"Not found": {"The requested company is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        except Payment.DoesNotExist:
            error = {"Not found": {"The requested payment is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            c = request.user.company

            payment = c.payment.get(pk=pk)
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Company.DoesNotExist:
            error = {"Not found": {"The requested company is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        except Payment.DoesNotExist:
            error = {"Not found": {"The requested payment is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)


class HookList(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        try:
            c = request.user.company

            hooks = c.hook.all()
            serializer = HookSerializer(hooks, many=True)

            return Response(serializer.data)

        except Company.DoesNotExist:
            response = HttpResponse
            response.status_code = 404

            return response()

    def post(self, request, format=None):
        serializer = HookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HookDetail(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk, format=None):
        try:
            c = request.user.company

            hook = c.hook.get(pk=pk)
            serializer = HookSerializer(hook)

            return Response(serializer.data)

        except Company.DoesNotExist:
            error = {"Not found": {"The requested company is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        except Hook.DoesNotExist:
            error = {"Not found": {"The requested hook is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, format=None):
        try:
            c = request.user.company

            hook = c.hook.get(pk=pk)
            serializer = HookSerializer(hook, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        except Company.DoesNotExist:
            error = {"Not found": {"The requested company is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        except Hook.DoesNotExist:
            error = {"Not found": {"The requested hook is not found."}}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

