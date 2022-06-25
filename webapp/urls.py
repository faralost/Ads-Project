from django.urls import path

from webapp.views import AdsListView, AdsToModerateListView

app_name = 'webapp'

urlpatterns = [
    path('', AdsListView.as_view(), name='index'),
    path('moderate_ads/', AdsToModerateListView.as_view(), name='ads_to_moderate_liist'),
]
