from django.contrib import admin

from webapp.models import Ad, Category


class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status']


admin.site.register(Ad, AdAdmin)
admin.site.register(Category)
