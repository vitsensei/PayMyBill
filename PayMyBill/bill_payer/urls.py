from django.urls import path

from . import views

app_name = 'bill_payer'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<str:company_name>', views.payments, name="payments"),
    path('home/<str:company_name>/<int:payment_id>', views.details, name="payment_details"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin")
]

