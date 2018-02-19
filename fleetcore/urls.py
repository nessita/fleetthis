# coding: utf-8

from django.contrib.auth.views import (
    LoginView,
    logout_then_login,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,

)
from django.urls import path
from fleetcore.views import (
    consumption_history,
    user_details,
    user_consumption_history,
)


urlpatterns = [
    path('history/', consumption_history, name='consumption-history'),
    path('details/<str:username>/', user_details, name='user-details'),
    path('history/<str:username>/', user_consumption_history,
         name='user-consumption-history'),
    path('login/', LoginView.as_view(template_name='fleetcore/login.html'),
         name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('password-reset/', password_reset,
         dict(template_name='fleetcore/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', password_reset_done,
         dict(template_name='fleetcore/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uuid:uidb64>/<str:token>/confirm/',
         password_reset_confirm,
         dict(template_name='fleetcore/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/', password_reset_complete,
         dict(template_name='fleetcore/password_reset_complete.html'),
         name='password_reset_complete'),
]
