# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

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
fleet_admin.register(Group, GroupAdmin)
fleet_admin.register(User, UserAdmin)


class UploadInvoiceForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class FleetAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(FleetAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(\d+)/upload-invoice/$',
                self.admin_site.admin_view(self.upload_invoice),
                name='upload-invoice')
        )
        return my_urls + urls

    def upload_invoice(self, request, fleet_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        fleet = get_object_or_404(self.queryset(request), pk=fleet_id)
        if request.method == 'POST':
            form = UploadInvoiceForm(request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = UploadInvoiceForm()

        context = {
            'form': form,
        }
        return TemplateResponse(request, [
            'admin/fleetcore/fleet/upload_invoice.html'
        ], context, current_app=self.admin_site.name)


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
fleet_admin.register(Fleet, FleetAdmin)
fleet_admin.register(Phone)
fleet_admin.register(Plan)
fleet_admin.register(UserProfile)
