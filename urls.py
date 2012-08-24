from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^fleetthis/', include('fleetthis.app.urls')),
    (r'^admin/(.*)', admin.site.root),
)
