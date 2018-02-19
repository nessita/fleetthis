# coding: utf-8

from __future__ import print_function, unicode_literals

from django.contrib import admin
from django.urls import include, path

import fleetcore.views


admin.autodiscover()


urlpatterns = [
    path('', fleetcore.views.home, name='home'),
    path('fleetcore/', include('fleetcore.urls')),
    path('admin/', admin.site.urls),
]
