from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import LoginForm

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            form_class=LoginForm, template_name="accounts/login_form.html"
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("logout/", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
]
