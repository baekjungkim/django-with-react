from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Post

# Class Based View
# post_list = ListView.as_view(model=Post)

# Function Based View
def post_list(request):
    # reqeust.GET
    # request.POST
    # request.FILES
    qs = Post.objects.all()
    q = request.GET.get("query", "")

    if q:
        qs = qs.filter(message__icontains=q)

    # print(qs.query)

    # instagram/templates/instagram/post_list.html
    return render(request, "instagram/post_list.html", {"post_list": qs, "q": q})


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:

    return render(request, "instagram/post_list.html", {})


def archives_year(request, year):
    return HttpResponse(f"{year}년 archives")


def archives_slug(request, slug):
    return HttpResponse(f"{slug} 입니다.")
