from django.core.management import call_command
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def do_update(request):
    """Trigger the deploy command."""
    # http authentication: bitbucket c4tup3cu
    call_command('deploy')
    return HttpResponse('OK')
