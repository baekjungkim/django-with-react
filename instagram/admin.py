from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Comment

# 등록방법 1
# admin.site.register(Post)

# 등록방법 2
# class PostAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(Post, PostAdmin)

# 등록방법 3
@admin.register(Post)  # Wrapping
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "photo_tag",
        "message",
        "message_length",
        "is_public",
        "author",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["id", "message"]
    list_filter = ["created_at", "is_public"]
    search_fields = ["message"]

    def photo_tag(self, post):
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' style='width: 72px;' />")
        return None

    def message_length(self, post):
        return f"{len(post.message)} 글자"

    message_length.short_description = "메세지 글자수"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
