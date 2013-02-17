from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class LeadershipRequiredTestCase(TestCase):
    urls = 'fleetusers.tests.test_urls'
    
    def setUp(self):
        self.url = reverse('test-leadership', args=['user'])
        self.admin = User.objects.create_user(username='admin',
                                              password='admin')
        self.admin.is_superuser = True
        self.admin.save()
        self.leader = User.objects.create_user(username='leader',
                                               password='leader')
        self.user = User.objects.create_user(username='user',
                                             password='user')
        user_profile = self.user.get_profile()
        user_profile.leader = self.leader
        user_profile.save()

    def test_admin_pass(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

    def test_leader_pass(self):
        self.client.login(username='leader', password='leader')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

    def test_anonymous_404(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_no_leader_404(self):
        self.client.login(username='user', password='user')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
