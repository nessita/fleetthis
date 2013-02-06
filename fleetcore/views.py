# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from fleetcore.models import Consumption


@login_required
def home(request):
    a_year_before = date.today() - timedelta(days=365)
    recent_consumptions = Consumption.objects.filter(
        phone__user=request.user,
        bill__billing_date__gte=a_year_before).order_by('-bill__billing_date')
    return TemplateResponse(request, template='fleetcore/index.html',
                            context={'consumptions': recent_consumptions})


@login_required
def consumption_history(request):
    consumptions = Consumption.objects.filter(
        phone__user=request.user).order_by('-bill__billing_date')
    return TemplateResponse(request, template='fleetcore/history.html',
                            context={'consumptions': consumptions})
