# coding: utf-8

from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.db import models
from django.forms.widgets import TextInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from fleetcore.forms import DeltaForm
from fleetcore.models import (
    Bill,
    Consumption,
    DataPack,
    Fleet,
    FleetUser,
    Penalty,
    Phone,
    Plan,
    SMSPack,
)
from fleetcore.sendbills import BillSummarySender


class BillAdminForm(forms.ModelForm):

    invoice = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(BillAdminForm, self).__init__(*args, **kwargs)
        if self.instance.parsing_date is not None:
            self.fields['invoice'] = forms.CharField(
                widget=forms.TextInput(attrs={'readonly': True, 'size': 70}),
                initial=self.instance.invoice_filename)

    class Meta:
        model = Bill
        fields = '__all__'


class PenaltyAdmin(admin.StackedInline):
    fieldsets = (
        (None, {'fields': (('plan', 'minutes', 'sms'),)}),
    )
    model = Penalty
    extra = 0


class BillAdmin(admin.ModelAdmin):

    form = BillAdminForm
    formfield_overrides = {
        models.TextField: {'widget': TextInput},
    }
    inlines = (PenaltyAdmin,)
    readonly_fields = (
        'taxes', 'consumptions_total', 'outcome_debt', 'outcome_total',
    )
    fieldsets = (
        (None, {
            'fields': (
                ('fleet', 'invoice'),
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
                ('taxes', 'consumptions_total',
                 'outcome_debt', 'outcome_total'),
                'notes',
            )
        }),
    )

    def get_urls(self):
        urls = super(BillAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<bill_id>\d+)/recalculate/$',
                self.admin_site.admin_view(self.recalculate),
                name='recalculate'),
            url(r'^(?P<bill_id>\d+)/notify-users/$',
                self.admin_site.admin_view(self.notify_users),
                name='notify-users'),
            url(r'^(?P<bill_id>\d+)/add-delta/$',
                self.admin_site.admin_view(self.add_delta),
                name='add-delta'),
        ]
        return my_urls + urls

    def save_model(self, request, obj, form, change):
        super(BillAdmin, self).save_model(request, obj, form, change)
        if obj.parsing_date is not None:
            return

        invoice = form.cleaned_data['invoice']
        error_msg = _('Invoice processed unsuccessfully. Error: ')
        try:
            obj.parse_invoice(invoice)
        except Bill.ParseError as e:
            messages.error(request, error_msg + str(e))
        else:
            self.recalculate(request, obj,
                             msg=_('Invoice processed successfully.'))

    def recalculate(self, request, obj=None, bill_id=None, msg=None):
        if obj is None:
            assert bill_id is not None, 'Bill id should not be None'
            obj = get_object_or_404(self.get_queryset(request), pk=bill_id)

        error_msg = _('Invoice processed unsuccessfully. Error: ')

        try:
            obj.calculate_penalties()
        except Bill.AdjustmentError as e:
            messages.error(request, error_msg + str(e))
        else:
            msg = msg or _('Penalties re-calculated successfully.')
            messages.success(request, msg)

        return HttpResponseRedirect('..')

    def notify_users(self, request, bill_id):
        obj = get_object_or_404(self.get_queryset(request), pk=bill_id)

        sender = BillSummarySender(bill=obj)

        if request.POST:
            try:
                sender.send_reports(dry_run=False)
            except Exception as e:
                msg = _('Notification error.')
                msg += ' Error: %s' % str(e)
                messages.error(request, msg)
            else:
                msg = _('Notifications sent successfully.')
                messages.success(request, msg)

            return HttpResponseRedirect('..')

        emails = sender.send_reports(dry_run=True)
        return TemplateResponse(request,
                                'admin/fleetcore/bill/notify_users.html',
                                dict(emails=emails))

    def add_delta(self, request, bill_id):
        obj = get_object_or_404(self.get_queryset(request), pk=bill_id)

        if request.method == 'POST':
            form = DeltaForm(request.POST)
            if form.is_valid():
                delta = form.cleaned_data['delta']
                obj.apply_delta(delta)
                msg = _('Delta %s added successfully.' % delta)
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = DeltaForm()

        return TemplateResponse(request,
                                'admin/fleetcore/bill/add_delta.html',
                                dict(form=form))


class ConsumptionAdmin(admin.ModelAdmin):
    """Admin class for Consumption."""
    search_fields = ('phone__user__username', 'phone__user__first_name',
                     'phone__user__last_name', 'bill__billing_date',)
    list_filter = ('bill', 'phone',)
    readonly_fields = ('total_min', 'total_sms')
    fieldsets = (
        (None, {
            'fields': ('phone', 'bill', 'plan'),
        }),
        ('Totals', {
            'fields': (('penalty_min', 'total_min'),
                       ('penalty_sms', 'total_sms'),
                       'total_before_taxes', 'taxes', 'extra',
                       'total_before_round', 'total')
        }),
        ('Data from provider', {
            'classes': ('collapse',),
            'fields': (
                ('reported_user', 'reported_plan', 'monthly_price'),
                ('services', 'refunds'),
                ('included_min', 'mins'),
                ('exceeded_min', 'exceeded_min_price'),
                ('ndl_min', 'ndl_min_price'),
                ('idl_min', 'idl_min_price'), ('sms', 'sms_price'),
                ('equipment_price', 'other_price'), 'reported_total',
            )
        }),
    )


class PhoneAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'user_full_name', 'current_plan', 'active', 'since',
    )
    list_filter = ('number', 'user')
    ordering = ('active_to', '-active_since',)

    def user_full_name(self, phone):
        return phone.user.get_full_name()

    def active(self, phone):
        return phone.active

    active.boolean = True

    def since(self, phone):
        if phone.active:
            result = str(phone.active_since)
        else:
            result = str(phone.active_to)
        return result


admin.site.register(Bill, BillAdmin)
admin.site.register(Consumption, ConsumptionAdmin)
admin.site.register(DataPack)
admin.site.register(Fleet)
admin.site.register(FleetUser)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Plan)
admin.site.register(SMSPack)
