# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin
from django.contrib.auth.models import User

from fleetthis.fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
    UserProfile,
)


admin.site.register(Bill)
admin.site.register(Consumption)
admin.site.register(Fleet)
admin.site.register(Phone)
admin.site.register(Plan)
admin.site.register(UserProfile)
