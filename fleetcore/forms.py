# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

from django import forms


class ReportForm(forms.Form):
    body = forms.CharField()
    subject = forms.CharField()
