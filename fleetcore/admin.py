# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from fleetusers.models import UserProfile
from fleetcore.models import (
    Bill,
    Consumption,
    Fleet,
    Penalty,
    Phone,
    Plan,
)
from fleetcore.sendbills import BillSummarySender


class PenaltyAdmin(admin.StackedInline):
    fieldsets = (
        (None, {'fields': (('plan', 'minutes', 'sms'),)}),
    )
    model = Penalty
    extra = 0


class BillAdmin(admin.ModelAdmin):

    inlines = (PenaltyAdmin,)
    readonly_fields = (
        'taxes', 'consumptions_total', 'outcome',
    )
    fieldsets = (
        (None, {
            'fields': (
                ('fleet', 'invoice', 'invoice_format'),
                ('parsing_date', 'upload_date'),
            )
        }),
        ('Data from provider', {
            'fields': (
                ('provider_number', 'billing_date'),
                ('billing_total', 'billing_debt'),
            )
        }),
        ('Taxes', {
            'fields': (
                ('internal_tax', 'iva_tax', 'other_tax'),
                ('taxes', 'consumptions_total', 'outcome'),
            )
        }),
    )

    def get_urls(self):
        urls = super(BillAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^(?P<bill_id>\d+)/process-invoice/$',
                self.admin_site.admin_view(self.process_invoice),
                name='process-invoice'),
            url(r'^(?P<bill_id>\d+)/notify-users/$',
                self.admin_site.admin_view(self.notify_users),
                name='notify-users'),
        )
        return my_urls + urls

    def process_invoice(self, request, bill_id):
        obj = get_object_or_404(self.queryset(request), pk=bill_id)
        error_msg = _('Invoice processed unsuccessfully. Error: ')

        try:
            obj.parse_invoice()
        except Bill.ParseError as e:
            messages.error(request, error_msg + unicode(e))

        try:
            obj.calculate_penalties()
        except Bill.AdjustmentError as e:
            messages.error(request, error_msg + unicode(e))
        else:
            msg = _('Invoice processed successfully.')
            messages.success(request, msg)

        return HttpResponseRedirect('..')

    def notify_users(self, request, bill_id):
        obj = get_object_or_404(self.queryset(request), pk=bill_id)

        sender = BillSummarySender(bill=obj)

        if request.POST:
            try:
                sender.send_reports(dry_run=False)
            except Exception as e:
                msg = _('Notification error.')
                msg += ' Error: %s' % unicode(e)
                messages.error(request, msg)
            else:
                msg = _('Notifications sent successfully.')
                messages.success(request, msg)

            return HttpResponseRedirect('..')

        emails = sender.send_reports(dry_run=True)
        return TemplateResponse(request,
                                'admin/fleetcore/bill/notify_users.html',
                                dict(emails=emails))


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
            'fields': (('penalty_min', 'total_min'),
                       'total_before_taxes', 'taxes', 'total_before_round',
                       ('total', 'payed'),)
        }),
        ('Data from provider', {
            'classes': ('collapse',),
            'fields': (
                'reported_user',
                ('reported_plan', 'monthly_price'),
                'included_min',
                ('services', 'refunds'),
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
