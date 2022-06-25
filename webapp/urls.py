from django.urls import path

from webapp.views.ad_views import AdsListView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView
from webapp.views.to_moderate_ad_views import AdsToModerateListView, AdToModerateDetailView, AdPublishView, AdRejectView

app_name = 'webapp'

urlpatterns = [
    path('', AdsListView.as_view(), name='index'),
    path('moderate_ads/', AdsToModerateListView.as_view(), name='ads_to_moderate_liist'),
    path('moderate_ads/<int:pk>/', AdToModerateDetailView.as_view(), name='ads_to_moderate_detail'),
    path('moderate_ads/<int:pk>/publish', AdPublishView.as_view(), name="ads_to_moderate_publish"),
    path('moderate_ads/<int:pk>/reject', AdRejectView.as_view(), name="ads_to_moderate_reject"),
    path('ad/create/', AdCreateView.as_view(), name='ads_create'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ads_detail'),
    path('ad/<int:pk>/update', AdUpdateView.as_view(), name='ads_update'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ads_delete'),
]
