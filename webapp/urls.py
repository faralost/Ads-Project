from django.urls import path, include

from webapp.views.ad_views import (
    AdsListView,
    AdCreateView,
    AdDetailView,
    AdUpdateView,
    AdDeleteView,
)
from webapp.views.to_moderate_ad_views import (
    AdsToModerateListView,
    AdToModerateDetailView,
    AdPublishView,
    AdRejectView,
)

app_name = 'webapp'

ads_urlpatterns = [
    path('create/', AdCreateView.as_view(), name='ads_create'),
    path('<int:pk>/', AdDetailView.as_view(), name='ads_detail'),
    path('<int:pk>/update', AdUpdateView.as_view(), name='ads_update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ads_delete'),
]

moderate_ads_urlpatterns =[
    path('', AdsToModerateListView.as_view(), name='ads_to_moderate_liist'),
    path('<int:pk>/', AdToModerateDetailView.as_view(), name='ads_to_moderate_detail'),
    path('<int:pk>/publish', AdPublishView.as_view(), name="ads_to_moderate_publish"),
    path('<int:pk>/reject', AdRejectView.as_view(), name="ads_to_moderate_reject"),
]

urlpatterns = [
    path('', AdsListView.as_view(), name='index'),
    path('ads/', include(ads_urlpatterns)),
    path('moderate_ads/', include(moderate_ads_urlpatterns)),
]
