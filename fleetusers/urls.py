# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', dict(template_name='users/login.html'),
        name='login'),
    url(r'^logout/$', 'logout', name='login'),
)
