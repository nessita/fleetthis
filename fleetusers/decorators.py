from functools import wraps

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import available_attrs


def leadership_required(view_func):
    """Decorator that checks logged in user has access to another user data.

    It requires the decorated view to take 'username' as first argument.
    It would raise a 404 if user is not allowed to get the details.

    """
    @wraps(view_func)
    def _decorated_view(request, username, *args, **kwargs):
        logged_in_user = request.user
        another_user = get_object_or_404(User, username=username)
        profile = another_user.get_profile()

        if request.user.is_superuser or profile.leader == request.user:
            return view_func(request, username, *args, **kwargs)
        else:
            raise Http404
    return _decorated_view
