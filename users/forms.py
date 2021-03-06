from django import forms
from allauth.socialaccount.forms import SignupForm
from . import models


class LoginForm(forms.Form):  # login form

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):  # 일반 signup form , forms.modelform 상속,
    class Meta:  # forms.Form 상속과는 다르게 forms.ModelForm 은 Meta class 와
        model = models.User  # model,
        fields = [  # fields 선언 해줘야 사용가능 model 내에 있더라도 field 선언안해주면 입력 form 생성불가
            "email",
            "name",
            "birthdate",
            "gender",
        ]
        widgets = {  # widget 명시 가능
            # "birthdate": forms.SelectDateWidget,
            "email": forms.EmailInput(attrs={"Placeholder": "Email"}),
        }

    password = forms.CharField(  # password, password1 은 model엔 없지만 별도의 form 을 생성후 아래 clean_password 를통해 비밀번호 두개를 받고 비교후 일치하면 user 의 password에 사용 가능
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmed Password"})
    )

    def clean_email(self):  # 이메일이 있는지 확인하는소스
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):  # password , password1 비교하는소스 위의 password form 참조
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


class SocialSignUpForm(
    SignupForm
):  # SignupForm은 위의 SignUpForm클래스가아닌 allauth.socialaccount.forms의 클래스로(스펠링의 대소문자와 상단 import 확인) 이 클래스를 상속해야
    name = forms.CharField(
        label="Name"
    )  # django-allauth 를 통한 social signup 시 해당 form을 사용가능함, 만약 위의 SignUpForm 처럼 forms.ModelForm 상속시 이중가입됨(social계정하나, 일반계정하나)
    gender = forms.ChoiceField(choices=models.User.GENDER_CHOICES)
    birthdate = forms.DateField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def save(self, request):
        user = super(SocialSignUpForm, self).save(request)
        user.name = self.cleaned_data["name"]
        user.gender = self.cleaned_data["gender"]
        user.birthdate = self.cleaned_data["birthdate"]
        # user.verify_email()
        user.save()
        return user
