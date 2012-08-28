from django.contrib import admin
from django.contrib.auth.models import User

from fleetthis.fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
)


admin.site.register(Bill)
admin.site.register(Consumption)
admin.site.register(Fleet)
admin.site.register(Phone)
admin.site.register(Plan)
