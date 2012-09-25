# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.response import SimpleTemplateResponse


def do_login(request):
    ##username = request.POST['username']
    ##password = request.POST['password']
    ##user = authenticate(username=username, password=password)
    ##if user is not None:
    ##    if user.is_active:
    ##        login(request, user)
    ##        # Redirect to a success page.
    ##    else:
    ##        # Return a 'disabled account' error message
    ##else:
    ##    # Return an 'invalid login' error message.
    return


@login_required
def home(request):
    return SimpleTemplateResponse('index.html')
