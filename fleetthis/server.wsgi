import os
import sys

from django.core.handlers.wsgi import WSGIHandler

# patch stdout since wsgi will not allow writting to stdout (it will 500)
sys.stdout = sys.stderr

curdir = os.path.abspath(os.path.dirname(__file__))
appdir = os.path.join(curdir, 'fleetthis')
if appdir not in sys.path:
    sys.path.insert(0, appdir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fleetthis.settings'


def application(environ, start_response):
    return WSGIHandler()
