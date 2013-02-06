# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from fleetcore.models import Consumption


@login_required
def home(request):
    recent_consumptions = Consumption.objects.filter(
        phone__user=request.user).order_by('-bill__billing_date')
    return TemplateResponse(request, template='index.html',
                            context={'consumptions': recent_consumptions})
