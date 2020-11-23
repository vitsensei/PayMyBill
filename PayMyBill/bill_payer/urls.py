from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:company_name>/', views.payments, name="payments"),
    path('<str:company_name>/<int:payment_id>', views.details, name="payment_details")
]

