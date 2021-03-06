import hashlib, hmac, base64, requests, time, json, uuid, random
from django.utils import translation
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import (
    FormView,
    DetailView,
    UpdateView,
    ListView,
    View,
    TemplateView,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms, mixins
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

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

def sign_up(request):
    name = request.POST.get('id_name')
    new_user = models.User.objects.create(
        name = name,
        
    )
    pass


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
        "image",
        "phone_number",
    )
    success_message = "Profile updated"
    
    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk':self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["name"].widget.attrs = {"label" : "name", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded","placeholder": "name"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["image"].widget.attrs = {"placeholder": "Image", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["phone_number"].widget.attrs = {"placeholder": "phone_number", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        
        form.fields["name"]
        return form


class UpdateMentorProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Mentor
    template_name = "users/update_mentor_profile.html"
    fields = (        
        "main_branch",
        "sub_branch",
        "company",
        "department",
        "career",      
    )
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        return self.request.user.mentor.first()
        
    def get_success_url(self):
        return reverse('users:mentor-profile', kwargs={'pk':self.request.user.mentor.first().pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["main_branch"].widget.attrs = {"placeholder": "main_branch", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["sub_branch"].widget.attrs = {"placeholder": "sub_branch", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["company"].widget.attrs = {"placeholder": "company", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["department"].widget.attrs = {"placeholder": "department", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["career"].widget.attrs = {"placeholder": "career", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}      
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
        return reverse('users:profile', kwargs={'pk':self.request.user.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Currnet password", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password", "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirmed new passowrd" , "class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"
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


@csrf_exempt
def ajax_buy_point(request):
    user = request.user
    merchant_value = request.POST.get("merchant_value")
    merchant_name = request.POST.get("merchant_name")
    point = models.Point(
        state=models.Point.STATE_ACCRUAL,
        product_name=merchant_name,
        value=merchant_value,
        user=user,
        date=timezone.now(),
    )
    point.save()
    user_model = models.User.objects.get(pk=request.POST.get("user_pk"))
    user_model.point += int(merchant_value)
    user_model.save()
    context = "done"
    return HttpResponse(json.dumps(context), content_type="application/json")


class UserPointView(TemplateView):
    template_name = "users/point.html"


class MentorSignUpView(FormView):
    template_name = "users/Mentorsignup.html"
    form_class = forms.MentorsignupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        mentor = models.Mentor.objects.create(
            user=self.request.user,
            main_branch=form.cleaned_data.get("main_branch"),
            sub_branch=form.cleaned_data.get("sub_branch"),
            company=form.cleaned_data.get("company"),
            department=form.cleaned_data.get("department"),
            career=form.cleaned_data.get("career"),
            address=form.cleaned_data.get("address"),
            address_name=form.cleaned_data.get("address_name"),
        )
        form.save()
        user_model = models.User.objects.get(id=self.request.user.id)
        user_model.is_mentor = True
        user_model.save()
        return super().form_valid(form)


def renderkakaomap(request):
    return render(request, "users/kakaomap.html")

class MentorListView(ListView):
    """ MentorListView Definition """
    model = models.Mentor
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "Mentors"
    template_name = 'users/mentor_list.html'
    
    def get_queryset(self):
        return models.Mentor.objects.filter(is_authorized=True)

class HomeMentorListView(ListView):
    """ MentorListView Definition """
    model = models.Mentor
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "Mentors"
    template_name = 'home.html'
    
    def get_queryset(self):
        return models.Mentor.objects.filter(is_authorized=True)
    
class ManageUserView(ListView):
    
    model = models.User
    template_name = "users/manage_users.html"
    paginate_by = 10
    paginate_orphans = 5
    ordering = "-created"
    context_object_name = "Mentors"
    
    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            return models.Mentor.objects.filter(user__is_superuser=False).filter(user__name__contains=search).order_by("-created")
        
        checked = self.request.GET.get("checked")
        if checked:
            if checked == "true":
                return models.Mentor.objects.filter(user__is_superuser=False).filter(is_authorized=True).order_by("-created")
            else:
                return models.Mentor.objects.filter(user__is_superuser=False).filter(is_authorized=False).order_by("-created")
        else:
            return models.Mentor.objects.filter(user__is_superuser=False).order_by("created")
        
@login_required
def manage_user(request):
    if request.user.is_superuser: # 관리자 여부
        try:
            user_pk = request.POST.getlist("user_pk")
            Mentor_pk = request.POST.getlist("mentor_pk")
            checkedbox = request.POST.getlist("checkedbox")
            for pk in Mentor_pk:
                Mentor = models.Mentor.objects.get(pk=pk)
                if pk in checkedbox:
                    Mentor.is_authorized = True
                    Mentor.user.is_mentor = True
                else:
                    Mentor.is_authorized = False
                    Mentor.user.is_mentor = False
                Mentor.save()
        except:
            pass
        return redirect(reverse("users:manage"))
    else:
        return redirect(reverse("core:home"))
    
class KakaoLoginTest(View):
    def get(self, request):
        REST_API_KEY = '21d002f9794143bd76e3fa58aab3af30'
        REDIRECT_URI = 'http://gomentorgo.shop/users/kakao/login/callback/'
        API_HOST = f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}'
        return redirect(API_HOST)
class KakaoException(Exception):
    pass    
def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = "21d002f9794143bd76e3fa58aab3af30"
        redirect_uri = "http://gomentorgo.shop/users/kakao/login/callback/"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            print("tokenerror")
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        get_email = profile_json.get("kakao_account").get("email")
        if get_email is None:
            print("emailerror")
            raise KakaoException
        try:
            user = models.User.objects.get(email=get_email)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect(reverse("core:home"))
        except models.User.DoesNotExist:
            return redirect(reverse("users:kakaosignup"))
        
    except KakaoException:
        return redirect(reverse("core:home"))
class KakaoSignUpView(FormView):  # 일반 회원가입 function 니꼬 소스 참조

    template_name = "users/signup_kakao.html"
    form_class = forms.kakaoSignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = "adfdalksjflqj"
        user = authenticate(
            self.request,
            username=email,
            password=password,
        )
        user.set_unusable_password();
        if user is not None:
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
        user.verify_email()
        return super().form_valid(form)   