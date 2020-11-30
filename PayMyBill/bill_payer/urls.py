from django.urls import path
from rest_framework.authtoken import views as rest_views

from . import views

app_name = 'bill_payer'

urlpatterns = [
    path("token", rest_views.obtain_auth_token),
    path("resources/company", views.CompanyDetail.as_view()),
    path('resources/payment', views.PaymentList.as_view()),
    path('resources/payment/<str:pk>', views.PaymentDetail.as_view()),
    path('resources/hook', views.HookList.as_view()),
    path('resources/hook/<str:pk>', views.HookDetail.as_view())
    # path('', views.index, name='index'),
    # path('home/<str:company_name>', views.payments, name="payments"),
    # path('home/<str:company_name>/<int:payment_id>', views.details, name="payment_details"),
    # path('signup/', views.signup, name="signup"),
    # path('signin/', views.signin, name="signin")
]

