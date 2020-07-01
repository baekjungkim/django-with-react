from django.urls import path
from . import views

app_name = "blog1"  # URL Reverse 에서 namespace 역할을 하게 됩니다.

urlpatterns = [
    path("", views.post_list, name="post_list"),
]
