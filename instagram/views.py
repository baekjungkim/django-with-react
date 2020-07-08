from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ArchiveIndexView, DetailView, ListView, YearArchiveView

from .forms import PostForm
from .models import Post

# https://docs.djangoproject.com/en/3.0/ref/request-response/
# HttpRequest.META : request 로 넘어오는 값들, ex) REMOTE_ADDR : The IP address of the client.
@login_required  # 로그인 인증이 되었다는 확인. 로그인 페이지가 구현되어있다면 로그인 페이지로 이동. 구현 안되어있으면 404페이지 이동
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인 User Instance
            # post.ip = request.META['REMOTE_ADDR']  # Client IP
            post.save()
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect(post)
    else:
        form = PostForm()
    return render(request, "instagram/post_form.html", {"form": form, "post": None})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 작성자 Check Tip!
    # Custom Decorator(장식자) 로 만들어서 사용할 수 있음.
    if post.author != request.user:
        messages.error(request, "작성자만 수정할 수 있습니다.")
        return redirect(post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "포스팅을 수정했습니다.")
            return redirect(post)
    else:
        form = PostForm(instance=post)
    return render(request, "instagram/post_form.html", {"form": form, "post": post})


# Class Based View
@method_decorator(login_required, name="dispatch")
# class PostListView(LoginRequiredMixin, ListView): # LoginRequiredMixin == login_required
class PostListView(ListView):
    model = Post
    paginate_by = 5
    q = ""

    def get_queryset(self):
        self.q = self.request.GET.get("query", "")
        qs = super().get_queryset()
        if self.q:
            qs = qs.filter(message__icontains=self.q)

        return qs

    def get_context_data(self):
        context = super().get_context_data()
        context["q"] = self.q
        return context


# @method_decorator(login_required)
# def dispatch(self, *args, **kwargs):
#     return super().dispatch(*args, **kwargs)


# post_list = login_required(PostListView.as_view())
post_list = PostListView.as_view()

# Function Based View
# @login_required  # 로그인 확인 장식자(Decorators)
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get("query", "")

#     if q:
#         qs = qs.filter(message__icontains=q)

#     messages.info(request, "messages 테스트")

#     # instagram/templates/instagram/post_list.html
#     return render(request, "instagram/post_list.html", {"post_list": qs, "q": q})


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


# CBV 방식으로 DetailView를 상속받아서 Override 해준다.
# DetailVeiw Class 의 SingleObjectMixin Override.
class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs


# 정의된 Class로 실행.
post_detail = PostDetailView.as_view()


# def archives_year(request, year):
#     return HttpResponse(f"{year}년 archives")

post_archive = ArchiveIndexView.as_view(
    model=Post, date_field="created_at", paginate_by=5, date_list_period="month",
)

post_archive_year = YearArchiveView.as_view(
    model=Post, date_field="created_at", make_object_list=True,
)

# def archives_slug(request, slug):
#     return HttpResponse(f"{slug} 입니다.")


def melon_list(request):
    return render(request, "instagram/melon_list.html", {})
