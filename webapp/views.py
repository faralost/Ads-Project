from django.views.generic import ListView

from webapp.models import Ad


class AdsListView(ListView):
    model = Ad
    template_name = 'ads/list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.exclude_to_delete_objects.all()
