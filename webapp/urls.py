from django.urls import path

from webapp.views import AdsListView, AdsToModerateListView, AdToModerateDetailView, AdPublishView

app_name = 'webapp'

urlpatterns = [
    path('', AdsListView.as_view(), name='index'),
    path('moderate_ads/', AdsToModerateListView.as_view(), name='ads_to_moderate_liist'),
    path('moderate_ads/<int:pk>/', AdToModerateDetailView.as_view(), name='ads_to_moderate_detail'),
    path('moderate_ads/<int:pk>/publish', AdPublishView.as_view(), name="ads_to_moderate_publish"),
]
