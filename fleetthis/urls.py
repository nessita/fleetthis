# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'fleetcore.views.home', name='home'),
    url(r'^fleetusers/', include('fleetusers.urls')),
    url(r'^fleetcore/', include('fleetcore.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
