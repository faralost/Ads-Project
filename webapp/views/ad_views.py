from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from webapp.forms import AdForm, CommentForm
from webapp.models import Ad, Comment
from webapp.views.base import SearchListView


class AdsListView(SearchListView):
    model = Ad
    template_name = 'ads/list.html'
    context_object_name = 'ads'
    paginate_by = 2
    search_fields = ['title__icontains', 'description__icontains']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(status=Ad.TO_DELETE).filter(status=Ad.PUBLISHED).order_by('-published_at')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['comments'] = Comment.objects.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=self.kwargs.get('pk'))
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.ad = ad
            comment.save()
            return redirect('webapp:ads_detail', pk=ad.pk)
        else:
            form = CommentForm()
        return render(request, 'ads/detail.html', {'form': form, 'ad': ad})


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
