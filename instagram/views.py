from django.shortcuts import render
from .models import Post

# reqeust.GET
# request.POST
# request.FILES
def post_list(request):
    qs = Post.objects.all()
    q = request.GET.get("query", "")

    if q:
        qs = qs.filter(message__icontains=q)

    print(qs.query)

    # instagram/templates/instagram/post_list.html
    return render(request, "instagram/post_list.html", {"post_list": qs, "q": q})
