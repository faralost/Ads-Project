from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from webapp.models import Ad


class AdsToModerateListView(PermissionRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/to_moderate_list.html'
    context_object_name = 'ads'
    paginate_by = 2

    def get_queryset(self):
        return Ad.exclude_to_delete_objects.filter(status=Ad.TO_MODERATE).order_by('-created_at')

    def has_permission(self):
        return self.request.user.is_staff


class AdToModerateDetailView(PermissionRequiredMixin, DetailView):
    model = Ad
    template_name = 'ads/to_moderate_detail.html'
    context_object_name = 'ad'

    def has_permission(self):
        return self.request.user.is_staff


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

