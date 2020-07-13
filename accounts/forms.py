# python 정규 표현식
# import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from nbformat import ValidationError

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = "__all__"
        fields = [
            "address",
            "zipcode",
        ]
        # exclude = [] # 특정 필드 배제 (사용하지 않기를 바람.)

    # form.py 내의 clean_필드명 함수를 통한 유효성 검사 및 값 변경
    # def clean_message(self):
    #     message = self.cleaned_data.get("message")
    #     if message:
    #         message = re.sub(r"[a-zA-Z]+", "", message)
    #     return message


class LoginForm(AuthenticationForm):
    answer = forms.IntegerField(help_text="3 + 3 = ?")

    def clean_answer(self):
        answer = self.cleaned_data.get("answer")
        if answer != 6:
            raise forms.ValidationError("떙!")
        return answer
