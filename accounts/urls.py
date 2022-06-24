from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UserDetailView, UsersListView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('change/', UserChangeView.as_view(), name='profile_change'),
    path('password_change', UserPasswordChangeView.as_view(), name='password_change'),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name="registration"),
    path('<slug:slug>/', UserDetailView.as_view(), name='detail_profile'),
]
