# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    leader = models.ForeignKey(User, related_name='leadering', null=True)

    def __unicode__(self):
        leader = self.leader
        if self.leader is not None:
            leader = self.leader.get_full_name() or self.leader
        if leader:
            leader = ' (leadered by %s)' % leader
        return '%s - %s%s' % (self.user, self.user.get_full_name(), leader)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
