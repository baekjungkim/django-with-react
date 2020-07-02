"""askcompany URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import global_settings
# from askcompany import settings
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

# class RootView(TemplateView):
#     template_name = "root.html"


# api_v1_patterns = [
#     # path()
# ]

urlpatterns = [
    # path("", TemplateView.as_view(template_name="root.html"), name="root"),
    # path("", RootView.as_view(), name="root"),
    path(
        "",
        RedirectView.as_view(
            # url="/instagram/"
            # Django 에서는 pattern_name 방식을 선호한다.
            pattern_name="instagram:post_list"  # instagram app 의 url name
        ),
        name="root",
    ),
    # path('api/v1/', include(api_v1_patterns)),
    path("admin/", admin.site.urls),  # URL Reverse
    path("accounts/", include("accounts.urls")),
    path("blog1/", include("blog1.urls")),
    path("instagram/", include("instagram.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

# settings.MEDIA_URL
# settings.MEDIA_ROOT
