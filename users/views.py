import hashlib, hmac, base64, requests, time, json, uuid, random
from django.utils import translation
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms, mixins
from django.views.decorators.csrf import csrf_exempt

# 이메일로 로그인
def send_sms(phone_number, text_to_content):
    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/ncp:sms:kr:264522537685:mentors/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = "Vo71wJ6C9daRaMlDMf8l"
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key

    secret_key = bytes("KkiFwCJVw70bx1oejRwKl7s4WCaoJfUIkvfAUvBD", "UTF-8")
    string = bytes(string_to_sign, "UTF-8")
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode("UTF-8")

    phone = phone_number

    message = text_to_content

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": string_base64,
    }

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "01088634192",
        "content": message,
        "messages": [{"to": phone}],
    }

    body = json.dumps(body)

    response = requests.post(api_url, headers=headers, data=body)
    response.raise_for_status()
    print(response)


def send_sms_to_verfy(phone_number):
    phone_number = str(phone_number)
    auth_number = str(random.randint(1000, 10000))
    text_to_content = "[Mentors] 인증 번호 [{}]를 입력해주세요.".format(auth_number)
    send_sms(phone_number, text_to_content)
    return auth_number


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


class MentorDetail(DetailView):
    """ MentorDetail Definition """

    model = models.Mentor
    context_object_name = "Mentor"


class MentorProfileView(DetailView):

    model = models.Mentor
    context_object_name = "Mentor"
    template_name = "users/mentor_profile.html"


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "users"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "name",
        "birthdate",
        "gender",
    )
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["name"].widget.attrs = {"placeholder": "name"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        return form


class UpdateMentorProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Mentor
    template_name = "users/update_Mentor_profile.html"
    fields = (
        "user",
        "main_branch",
        "sub_branch",
        "company",
        "department",
        "career",
        "is_authorized",
        "is_supermento",
    )
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["user"].widget.attrs = {"placeholder": "user"}
        form.fields["main_branch"].widget.attrs = {"placeholder": "main_branch"}
        form.fields["sub_branch"].widget.attrs = {"placeholder": "sub_branch"}
        form.fields["company"].widget.attrs = {"placeholder": "company"}
        form.fields["department"].widget.attrs = {"placeholder": "department"}
        form.fields["career"].widget.attrs = {"placeholder": "career"}
        form.fields["is_authorized"].widget.attrs = {"placeholder": "is_authorized"}
        form.fields["is_supermento"].widget.attrs = {"placeholder": "is_supermento"}

        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update_password.html"
    success_message = "Password updated"

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Currnet password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirmed new passowrd"
        }
        return form


@csrf_exempt
def ajax_sms_verfy(request):
    phone_number = request.POST.get("phone_number")
    auth_number = send_sms_to_verfy(phone_number)
    context = {
        "auth_number": auth_number,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def ajax_sms_check(request):
    auth_number = request.POST.get("auth_number")
    get_auth_number = request.POST.get("get_auth_number")
    result = ""
    if auth_number == get_auth_number:
        result = "성공"
    else:
        result = "실패"
    context = {"result": result}
    return HttpResponse(json.dumps(context), content_type="application/json")


class mentorsign:
    pass


def search(request):
    pass
