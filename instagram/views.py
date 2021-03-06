from os.path import altsep

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ArchiveIndexView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    YearArchiveView,
)

from .forms import PostForm
from .models import Post

# https://docs.djangoproject.com/en/3.0/ref/request-response/
# HttpRequest.META : request 로 넘어오는 값들, ex) REMOTE_ADDR : The IP address of the client.
# @login_required  # 로그인 인증이 되었다는 확인. 로그인 페이지가 구현되어있다면 로그인 페이지로 이동. 구현 안되어있으면 404페이지 이동
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # 현재 로그인 User Instance
#             # post.ip = request.META['REMOTE_ADDR']  # Client IP
#             post.save()
#             messages.success(request, "포스팅을 저장했습니다.")
#             return redirect(post)
#     else:
#         form = PostForm()
#     return render(request, "instagram/post_form.html", {"form": form, "post": None})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, "포스팅을 저장했습니다.")
        return super().form_valid(form)


post_new = PostCreateView.as_view()

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     # 작성자 Check Tip!
#     # Custom Decorator(장식자) 로 만들어서 사용할 수 있음.
#     if post.author != request.user:
#         messages.error(request, "작성자만 수정할 수 있습니다.")
#         return redirect(post)

#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save()
#             messages.success(request, "포스팅을 수정했습니다.")
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
#     return render(request, "instagram/post_form.html", {"form": form, "post": post})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, "포스팅을 수정했습니다.")
        return super().form_valid(form)

    # 사용자 인증 기능.
    def dispatch(self, request, *args, **kwargs):
        # self.object 에 현재 post object를 담는다.
        self.object = self.get_object()
        # post object의 author 와 로그인 user를 비교
        if not self.object.author == request.user:
            # 같지 않으면 메시지 출력
            messages.error(request, "작성자만 수정할 수 있습니다.")
            # 상세 화면으로 이동.
            return redirect(self.object)
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


post_edit = PostUpdateView.as_view()


# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         post.delete()
#         messages.success(request, "포스팅을 삭제했습니다.")
#         return redirect("instagram:post_list")

#     return render(request, "instagram/post_confirm_delete.html", {"post": post})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # success_url = reverse("instagram:post_list")
    # def get_success_url(self):
    #     return reverse("instagram:post_list")
    success_url = reverse_lazy("instagram:post_list")

    # 사용자 인증 기능.
    def dispatch(self, request, *args, **kwargs):
        # self.object 에 현재 post object를 담는다.
        self.object = self.get_object()
        # post object의 author 와 로그인 user를 비교
        if not self.object.author == request.user:
            # 같지 않으면 메시지 출력
            messages.error(request, "작성자만 삭제할 수 있습니다.")
            # 상세 화면으로 이동.
            return redirect(self.object)
        return super(PostDeleteView, self).dispatch(request, *args, **kwargs)


post_delete = PostDeleteView.as_view()

# Class Based View
# @method_decorator(login_required, name="dispatch")
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
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
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

    # 로그인 안했으면 비공개 포스팅은 볼 수 없다.
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
