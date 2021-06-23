from django import forms
from allauth.socialaccount.forms import SignupForm
from . import models


class LoginForm(forms.Form):  # login form

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "bg-gray-200 border-2 border-gray-100 focus:outline-none bg-gray-100 block w-full py-2 px-4 rounded-lg focus:border-gray-700 my-2",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "bg-gray-200 border-2 border-gray-100 focus:outline-none bg-gray-100 block w-full py-2 px-4 rounded-lg focus:border-gray-700 my-2",
            }
        ),
    )

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
    password = forms.CharField(  # password, password1 은 model엔 없지만 별도의 form 을 생성후 아래 clean_password 를통해 비밀번호 두개를 받고 비교후 일치하면 user 의 password에 사용 가능
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmed Password",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        )
    )
    auth_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "인증번호",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        )
    )

    class Meta:  # forms.Form 상속과는 다르게 forms.ModelForm 은 Meta class 와
        model = models.User  # model,
        fields = [  # fields 선언 해줘야 사용가능 model 내에 있더라도 field 선언안해주면 입력 form 생성불가
            "email",
            "name",
            "birthdate",
            "image",
            "gender",
            "phone_number",
        ]
        widgets = {  # widget 명시 가능
            # "birthdate": forms.SelectDateWidget,
            "name": forms.TextInput(
                attrs={
                    "placeholder": "이름",
                    "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "이메일",
                    "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
                }
            ),
            "birthdate": forms.DateInput(
                attrs={
                    "placeholder": "생년월일",
                    "class": "w-full px-5  py-1 text-gray-700 bg-gray-200 rounded",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "placeholder": "프로필 이미지",
                    "class": "w-full px-2 py-1 text-gray-700 bg-gray-200 rounded",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "placeholder": "성별",
                    "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
                }
            ),
            "phone_number": forms.NumberInput(
                attrs={
                    "placeholder": "번호",
                    "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
                }
            ),
        }
        fields = (
            "email",
            "password",
            "password1",
            "name",
            "birthdate",
            "image",
            "gender",
            "phone_number",
            "auth_number",
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
        user.is_mentor = False
        user.set_password(password)
        user.save()


class SocialSignUpForm(
    SignupForm
):  # SignupForm은 위의 SignUpForm클래스가아닌 allauth.socialaccount.forms의 클래스로(스펠링의 대소문자와 상단 import 확인) 이 클래스를 상속해야
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
        )
    )
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "이름",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        ),
    )  # django-allauth 를 통한 social signup 시 해당 form을 사용가능함, 만약 위의 SignUpForm 처럼 forms.ModelForm 상속시 이중가입됨(social계정하나, 일반계정하나)
    image = forms.ImageField(
        label="Profile Image",
        widget=forms.FileInput(
            attrs={
                "placeholder": "프로필 이미지",
                "class": "w-full px-2 py-1 text-gray-700 bg-gray-200 rounded",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=models.User.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "placeholder": "성별",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        ),
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "생년월일",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        )
    )
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "번호",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        )
    )
    auth_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "인증번호",
                "class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded",
            }
        )
    )

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
        user.phone_number = self.cleaned_data["phone_number"]
        user.image = self.cleaned_data["image"]
        user.is_mentor = False
        # user.verify_email()
        user.save()
        return user


class MentorsignupForm(forms.ModelForm):
    class Meta:
        model = models.Mentor
        fields = [
            "main_branch",
            "sub_branch",
            "company",
            "department",
            "career",
            "address",
            "address_name",
        ]
        widgets = {  # widget 명시 가능
            # "birthdate": forms.SelectDateWidget,
            "main_branch": forms.Select(
                attrs={"class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "sub_branch": forms.Select(
                attrs={"class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "company": forms.TextInput(
                attrs={"class": "w-full px-5  py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "department": forms.TextInput(
                attrs={"class": "w-full px-2 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "career": forms.Textarea(
                attrs={"class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "address": forms.TextInput(
                attrs={"class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "address_name": forms.TextInput(
                attrs={"class": "w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].widget.attrs["readonly"] = True
        self.fields["address_name"].widget.attrs["readonly"] = True
        self.fields["address"].widget.attrs[
            "placeholder"
        ] = "상단의 지도열어서 주소입력하기 버튼을 통해 입력하여 주십시오"
        self.fields["address_name"].widget.attrs[
            "placeholder"
        ] = "상단의 지도열어서 주소입력하기 버튼을 통해 입력하여 주십시오"
        self.fields["address"].widget.attrs["readonly"] = True
        self.fields["address_name"].widget.attrs["readonly"] = True
        # self.fields["address"].widget.error_messages = {""}
        # self.fields["address_name"].widget.attrs["readonly"] = True

    # def clean_user(self):
    #     email = self.request.user.objects.get("email")
    #     try:
    #         useremaiil = models.User.objects.get(email=email)
    #         raise forms.ValidationError(
    #             "That User is already taken", code="existing_user"
    #         )
    #     except models.User.DoesNotExist:
    #         return email

    def save(self, *args, **kwargs):
        mentor = super().save(commit=False)