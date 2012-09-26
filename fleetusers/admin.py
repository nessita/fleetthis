# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from fleetusers.models import (
    UserProfile,
)


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
##admin.site.unregister(User)
##admin.site.register(User, UserAdmin)

admin.site.register(UserProfile)
