from django.contrib import admin
from django.contrib.auth.models import User

from fleetthis.models import Plan, Phone


admin.site.register(Plan)
admin.site.register(Phone)
