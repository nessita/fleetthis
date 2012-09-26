# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import patterns
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from fleetusers.models import UserProfile
from fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
)


class FleetCoreAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super(FleetCoreAdminSite, self).get_urls()
        my_urls = patterns('',
            (r'^my_view/$', self.admin_view(self.my_view))
        )
        return my_urls + urls

    def my_view(self, request):
        # custom view which should return an HttpResponse
        print('WORKED')


fleet_admin = FleetCoreAdminSite(name='fleetcore-admin')


class ConsumptionAdmin(admin.ModelAdmin):
    """Admin class for Consumption."""
    search_fields = ('phone__user__username', 'phone__user__first_name',
                     'phone__user__last_name', 'bill__billing_date',)
    list_filter = ('bill', 'phone',)
    fieldsets = (
        (None, {
            'fields': ('phone', 'bill',)
        }),
        ('Totals', {
            'fields': ('total_before_taxes', 'taxes', 'total_before_round',
                       ('total', 'payed'),)
        }),
        ('Factura', {
            'classes': ('collapse',),
            'fields': (
                'reported_user', 'reported_plan', 'monthly_price',
                ('services', 'refunds'), 'included_min',
                ('exceeded_min', 'exceeded_min_price'),
                ('ndl_min', 'ndl_min_price'),
                ('idl_min', 'idl_min_price'), ('sms', 'sms_price'),
                ('equipment_price', 'other_price'), 'reported_total',
            )
        }),
    )


fleet_admin.register(Bill)
fleet_admin.register(Consumption, ConsumptionAdmin)
fleet_admin.register(Fleet)
fleet_admin.register(Phone)
fleet_admin.register(Plan)
fleet_admin.register(User)
fleet_admin.register(UserProfile)
