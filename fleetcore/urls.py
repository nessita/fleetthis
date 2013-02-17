# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'fleetcore.views',
    #url(r'^$', 'home', name='home'),
    url(r'^history/$', 'consumption_history', name='consumption-history'),
    url(r'^details/(?P<username>[\w-]+)/$', 'user_details',
        name='user-details'),
    url(r'^history/(?P<username>[\w-]+)/$', 'user_consumption_history',
        name='user-consumption-history'),
)
