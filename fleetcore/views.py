# coding: utf-8

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from fleetcore.decorators import leadership_required
from fleetcore.models import Consumption


User = get_user_model()


def _render_user_information(request, user):
    a_year_before = date.today() - timedelta(days=365)
    recent_consumptions = Consumption.objects.filter(
        phone__user=user,
        bill__billing_date__gte=a_year_before).order_by('-bill__billing_date')
    return render(
        request, 'fleetcore/index.html',
        {'current_user': user, 'consumptions': recent_consumptions})


def _render_user_history(request, user):
    consumptions = Consumption.objects.filter(
        phone__user=user).order_by('-bill__billing_date')
    return render(
        request, 'fleetcore/history.html',
        {'current_user': user, 'consumptions': consumptions})


@login_required
def home(request):
    return _render_user_information(request, request.user)


@login_required
@leadership_required
def user_details(request, username):
    user = get_object_or_404(User, username=username)
    return _render_user_information(request, user)


@login_required
def consumption_history(request):
    return _render_user_history(request, request.user)


@login_required
@leadership_required
def user_consumption_history(request, username):
    user = get_object_or_404(User, username=username)
    return _render_user_history(request, user)
