from django.conf import settings  # settings import
from django.core.validators import (
    MinLengthValidator,
)  # 되로록이면 valid 함수를 만들지말고 되어있는것을 사용하자
from django.db import models
from django.urls import reverse

# min_length_validator = MinLengthValidator(3)
# min_length_validator("he")  # forms.ValidationError


class Post(models.Model):

    """ Post Model """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # settings 의 AUTH_USER_MODEL, USER MODEL이 변경될 수 있기 때문
        on_delete=models.CASCADE,
        verbose_name="작성자",
    )
    message = models.TextField(validators=[MinLengthValidator(10)])
    photo = models.ImageField(blank=True, upload_to="instagram/post/%Y/%m/%d")
    # ManyToMany Field
    tag_set = models.ManyToManyField("Tag", blank=True)
    is_public = models.BooleanField(default=False, verbose_name="공개여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Java의 toString
    def __str__(self):

        # Python low Version
        # return "Custom Post object ({})".format(self.id)

        # Python 3.7
        # return f"Custom Post object ({self.id})"

        return self.message

    # URL Reverse 지정
    # URL Reverse를 간단하게 사용할 수 있음
    # post_list.html template 참조
    def get_absolute_url(self):
        return reverse("instagram:post_detail", args=[self.pk])

    class Meta:
        ordering = ["-id"]

    # def message_length(self):
    #     return len(self.message)

    # message_length.short_description = "메세지 글자수"


class Comment(models.Model):

    """ Comment Model """

    post = models.ForeignKey(
        # "instagram.Post"
        # "Post"
        Post,
        on_delete=models.CASCADE,
        limit_choices_to={"is_public": True},
    )  # post_id 필드 생성
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.message


class Tag(models.Model):

    """ Tag Model """

    # post_set = models.ManyToManyField(Post)

    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
