from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from webapp.forms import AdForm
from webapp.models import Ad


class AdsListView(ListView):
    model = Ad
    template_name = 'ads/list.html'
    context_object_name = 'ads'
    paginate_by = 2

    def get_queryset(self):
        return Ad.exclude_to_delete_objects.filter(status=Ad.PUBLISHED).order_by('-published_at')


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/detail.html'
    context_object_name = 'ad'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status == Ad.PUBLISHED or self.request.user == self.object.author:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            raise PermissionDenied


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    template_name = 'ads/create.html'
    form_class = AdForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:ads_detail", kwargs={"pk": self.object.pk})


class AdUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ad
    template_name = 'ads/update.html'
    form_class = AdForm

    def form_valid(self, form):
        form.instance.status = Ad.TO_MODERATE
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:ads_detail", kwargs={"pk": self.get_object().pk})

    def has_permission(self):
        return self.request.user == self.get_object().author and self.get_object().status != Ad.REJECTED


class AdDeleteView(PermissionRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/delete.html'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return self.request.user == self.get_object().author