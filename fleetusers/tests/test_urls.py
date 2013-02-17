from django.conf.urls import patterns, include, url
from django.http import HttpResponse

from fleetusers.decorators import leadership_required


def home(request):
    return HttpResponse('Home')


@leadership_required
def test_view(request, username):
    return HttpResponse('OK')


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^test-leadership-required/(?P<username>[\w-]+)/$', test_view,
        name='test-leadership'),
)
