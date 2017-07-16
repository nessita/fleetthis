# coding: utf-8

from django.conf.urls import url
from django.contrib.auth.views import (
    login,
    logout_then_login,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,

)
from fleetcore.views import (
    consumption_history,
    user_details,
    user_consumption_history,
)


urlpatterns = [
    url(r'^history/$', consumption_history, name='consumption-history'),
    url(r'^details/(?P<username>[\w-]+)/$', user_details,
        name='user-details'),
    url(r'^history/(?P<username>[\w-]+)/$', user_consumption_history,
        name='user-consumption-history'),
    url(r'^login/$', login, dict(template_name='fleetcore/login.html'),
        name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^password-reset/$', password_reset,
        dict(template_name='fleetcore/password_reset.html'),
        name='password-reset'),
    url(r'^password-reset/done/$', password_reset_done,
        dict(template_name='fleetcore/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^password-reset/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/confirm/$',
        password_reset_confirm,
        dict(template_name='fleetcore/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete,
        dict(template_name='fleetcore/password_reset_complete.html'),
        name='password_reset_complete'),
]
