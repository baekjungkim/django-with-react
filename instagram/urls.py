from django.urls import path, re_path, register_converter
from django.urls.converters import StringConverter

from . import views


class YearConverter:
    regex = r"20\d{2}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


class SlugUnicodeConverter(StringConverter):
    regex = r"[-\w]+"


register_converter(YearConverter, "year")
register_converter(SlugUnicodeConverter, "slug")

app_name = "instagram"  # URL Reverse 에서 namespace 역할을 하게 됩니다.

urlpatterns = [
    path("", views.post_list),
    # re_path(r"(?P<pk>\d+)/$", views.post_detail),
    path("<int:pk>/", views.post_detail),
    # path("archives/<int:year>/", views.archives_year),
    path("archives/<year:year>/", views.archives_year),
    # re_path(r"archives/(?P<year>\d{4})/", views.archives_year),
    # path("archives/<slug:slug>/", views.archives_slug),
]
