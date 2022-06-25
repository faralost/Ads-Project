from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from webapp.models import Ad


class AdsListView(ListView):
    model = Ad
    template_name = 'ads/list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.exclude_to_delete_objects.filter(status=Ad.PUBLISHED).order_by('-published_at')


class AdsToModerateListView(ListView):
    model = Ad
    template_name = 'ads/to_moderate_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.exclude_to_delete_objects.filter(status=Ad.TO_MODERATE).order_by('-created_at')


class AdToModerateDetailView(DetailView):
    model = Ad
    template_name = 'ads/to_moderate_detail.html'
    context_object_name = 'ad'


class AdPublishView(View):
    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        print(ad.status)
        if ad.status != Ad.PUBLISHED:
            ad.status = Ad.PUBLISHED
            ad.save()
            answer = 'Опубликован'
        else:
            answer = 'Уже был опубликован'
        data = {
            "answer": answer
        }
        return JsonResponse(data, safe=False)
