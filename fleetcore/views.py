# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

import fleetcore


@login_required
def home(request):
    return TemplateResponse(request, template='index.html',
                            context=dict(app_name=fleetcore.NAME))
