import os
import sys

import django.core.handlers.wsgi


INTERP = "/home/nessita/fleetthis/env/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# patch stdout since wsgi will not allow writting to stdout (it will 500)
sys.stdout = sys.stderr

cwd = os.getcwd()
appdir = cwd + '/fleetthis'
sys.path.insert(0, appdir)
sys.path.append(cwd)

#cwd = os.path.abspath(os.path.dirname(__file__))
#appdir = os.path.join(cwd, 'fleetthis')
#if appdir not in sys.path:
#    sys.path.insert(0, appdir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fleetthis.settings'


def application(environ, start_response):
    #start_response('200 OK', [('Content-type', 'text/plain')])
    #return ["Hello, world HOLA"]
    return django.core.handlers.wsgi.WSGIHandler()
