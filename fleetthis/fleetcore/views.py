# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.template.response import SimpleTemplateResponse


def home(request):
    return SimpleTemplateResponse('index.html')
