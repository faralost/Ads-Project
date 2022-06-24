from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['avatar', 'github_profile', 'about', 'slug']


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


User = get_user_model()
admin.site.unregister(User)


admin.site.register(User, ProfileAdmin)
