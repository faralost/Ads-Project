from django.urls import path

from webapp.views import AdsListView

app_name = 'webapp'

urlpatterns = [
    path('', AdsListView.as_view(), name='index'),
]
