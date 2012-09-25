# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'fleetthis.fleetcore.views',
    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'do_login', name='login'),
)
