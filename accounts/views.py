from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm, \
    ProfileCreationForm
from webapp.models import Ad

User = get_user_model()


def register(request):
    if request.method == "POST":
        u_form = MyUserCreationForm(request.POST)
        p_form = ProfileCreationForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            login(request, user)
            return redirect('webapp:index')
    else:
        u_form = MyUserCreationForm()
        p_form = ProfileCreationForm()
    return render(request, 'accounts/registration.html', {'u_form': u_form, 'p_form': p_form})


class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'
    slug_field = 'profile__slug'

    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = get_object_or_404(User, profile__slug=self.kwargs.get('slug'))
        if self.request.user == user:
            context['ads'] = user.ads.select_related(
                'author', 'author__profile', 'category'
            ).exclude(
                status=Ad.TO_DELETE
            )
        else:
            context['ads'] = user.ads.select_related(
                'author', 'author__profile', 'category'
            ).filter(
                status=Ad.PUBLISHED)
        return context


class UsersListView(PermissionRequiredMixin, ListView):
    template_name = 'accounts/users_list.html'
    model = User
    permission_required = 'accounts.view_profile'

    def get_queryset(self):
        return super().get_queryset().exclude(is_superuser=True)


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'accounts/user_change.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:detail_profile', kwargs={'slug': self.object.profile.slug})


class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:detail_profile', kwargs={'slug': self.object.profile.slug})
