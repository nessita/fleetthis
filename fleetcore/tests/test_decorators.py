from django.conf.urls import patterns, url
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase

from fleetcore.decorators import leadership_required

User = get_user_model()


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


class LeadershipRequiredTestCase(TestCase):
    urls = 'fleetcore.tests.test_decorators'

    def setUp(self):
        self.url = reverse('test-leadership', args=['user'])
        self.admin = User.objects.create_user(username='admin',
                                              password='admin')
        self.admin.is_superuser = True
        self.admin.save()
        self.leader = User.objects.create_user(
            username='leader', password='leader')
        self.user = User.objects.create_user(
            username='user', password='user', leader=self.leader)

    def test_admin_pass(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

    def test_leader_pass(self):
        self.client.login(username='leader', password='leader')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

    def test_anonymous_404(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_no_leader_404(self):
        self.client.login(username='user', password='user')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
