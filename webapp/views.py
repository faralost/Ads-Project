from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from webapp.forms import AdCreateForm
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
        if ad.status != Ad.PUBLISHED:
            ad.status = Ad.PUBLISHED
            ad.published_at = timezone.now()
            ad.save()
            answer = 'Опубликован'
        else:
            answer = 'Уже был опубликован'
        data = {
            "answer": answer
        }
        return JsonResponse(data, safe=False)


class AdRejectView(View):
    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        if ad.status != Ad.REJECTED:
            ad.status = Ad.REJECTED
            ad.save()
            answer = 'Отклонен'
        else:
            answer = 'Уже был отклонен'
        data = {
            "answer": answer
        }
        return JsonResponse(data, safe=False)


class AdCreateView(CreateView):
    model = Ad
    template_name = 'ads/create.html'
    form_class = AdCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
