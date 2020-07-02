from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

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


# FBV 방식
# def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     # try:
#     #     post = Post.objects.get(pk=pk)  # DoesNotExist 예외
#     # except Post.DoesNotExist:
#     #     raise Http404

#     post = get_object_or_404(Post, pk=pk)

#     return render(request, "instagram/post_detail.html", {"post": post,})

# CBV 방식
# post_detail = DetailView.as_view(
#     model=Post, queryset=Post.objects.filter(is_public=True)
# )


class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs


post_detail = PostDetailView.as_view()


def archives_year(request, year):
    return HttpResponse(f"{year}년 archives")


# def archives_slug(request, slug):
#     return HttpResponse(f"{slug} 입니다.")
