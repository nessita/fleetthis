# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from fleetusers.models import UserProfile
from fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Phone,
    Plan,
)


class BillAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(BillAdmin, self).get_urls()
        my_urls = patterns(
            '', url(r'^(\d+)/process-invoice/$',
                    self.admin_site.admin_view(self.process_invoice),
                    name='process-invoice')
        )
        return my_urls + urls

    def process_invoice(self, request, bill_id):
        if not self.has_change_permission(request):
            raise PermissionDenied

        bill = get_object_or_404(self.queryset(request), pk=bill_id)
        try:
            bill.parse_invoice()
        except Bill.ParseError as e:
            msg = _('Invoice processed unsuccessfully.')
            msg += ' Error: %s' % unicode(e)
            messages.error(request, msg)
        else:
            msg = _('Invoice processed successfully.')
            messages.success(request, msg)

        response = HttpResponseRedirect('..')
        return response


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
        ('Data from provider', {
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


admin.site.register(Bill, BillAdmin)
admin.site.register(Consumption, ConsumptionAdmin)
admin.site.register(Fleet)
admin.site.register(Phone)
admin.site.register(Plan)
admin.site.register(UserProfile)
