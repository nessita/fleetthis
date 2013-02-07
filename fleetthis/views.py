from django.core.management import call_command
from django.http import HttpResponse


def do_update(request):
    """Trigger the deploy command."""
    # http authentication: bitbucket c4tup3cu
    call_command('deploy')
    return HttpResponse('OK')
