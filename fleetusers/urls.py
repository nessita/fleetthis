# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse


urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', dict(template_name='users/login.html'),
        name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^password-reset/$', 'password_reset',
        dict(template_name='users/password_reset.html'),
        name='password-reset'),
    url(r'^password-reset/done/$', 'password_reset_done',
        dict(template_name='users/password_reset_done.html')),
    url(r'^password-reset/(?P<uidb36>[\w-]+)/(?P<token>[\w-]+)/confirm/$',
        'password_reset_confirm',
        dict(template_name='users/password_reset_confirm.html'),
        name='password-reset-confirm'),
    url(r'^password-reset/complete/$', 'password_reset_complete',
        dict(template_name='users/password_reset_complete.html')),
)
