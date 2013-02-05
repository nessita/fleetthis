import os
import sys

INTERP = "/home/nessita/fleetthis/env/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# patch stdout since wsgi will not allow writting to stdout (it will 500)
sys.stdout = sys.stderr

cwd = os.getcwd()
appdir = os.path.join(cwd, 'fleetthis')
if appdir not in sys.path:
    sys.path.insert(0, appdir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fleetthis.settings'

import django
from django.conf import settings

DEBUG_OUTPUT = """Hello World!

Running Python version: %s

Python path is: %s

Current dir is: %s

App dir is: %s

Django version %s, DEBUG is set to %s

"""


def debug_application(environ, start_response):
    output = DEBUG_OUTPUT % (sys.version, sys.path, cwd, appdir,
                             django.get_version(), settings.DEBUG)
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response('200 OK', response_headers)
    return [output]


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

##from paste.exceptions.errormiddleware import ErrorMiddleware
##application = ErrorMiddleware(application, debug=True)
