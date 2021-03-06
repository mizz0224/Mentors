from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


# 이메일로 로그인
class LoginView(FormView):  # 일반 login view, 니꼬 소스 참조

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
        return super().form_valid(form)


def log_out(request):  # 일반 logout function 니꼬 소스 참조
    logout(request)
    return redirect(reverse("core:home"))


# 일반 signup view 랑 social social 차이는 대체로 form 은 같으나, sign up view 에만 비밀번호 입력과확인이있음(password / password1)
class SignUpView(FormView):  # 일반 회원가입 function 니꼬 소스 참조

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(
            self.request,
            username=email,
            password=password,
        )
        if user is not None:
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
        user.verify_email()
        return super().form_valid(form)


class SocialSignUpView(FormView):  # social signup view

    template_name = "users/socialsignup.html"
    form_class = forms.SocialSignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(
            self.request,
            username=email,
            password=password,
        )
        if user is not None:
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))
