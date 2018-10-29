# coding: utf-8

from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    logout_then_login,
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
    path('password-reset/',
         PasswordResetView.as_view(
            template_name='fleetcore/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
            template_name='fleetcore/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uuid:uidb64>/<str:token>/confirm/',
         PasswordResetConfirmView.as_view(
            template_name='fleetcore/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(
            template_name='fleetcore/password_reset_complete.html'),
         name='password_reset_complete'),
]
