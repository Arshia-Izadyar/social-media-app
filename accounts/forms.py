from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

# from allauth.account.forms import SignupForm
from django.utils.translation import gettext as _

from .models import User
from utils.validators import email_validation, phone_validation


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("phone_number",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


# class MyCustomSignupForm(SignupForm):
#     phone_number = forms.CharField(
#         label=_("Phone Number"),
#         min_length=11,
#         widget=forms.TextInput(attrs={"placeholder": _("Phone Number"), "autocomplete": "phone number"}),
#     )

#     def save(self, request):
#         user = super(MyCustomSignupForm, self).save(request)

#         user.phone_number = self.cleaned_data["phone_number"]
#         user.save()

#         return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("bio", "location", "birth_day")


class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(validators=[email_validation.validate_email])
    phone_number = forms.CharField(validators=[phone_validation.validate_phone_number], max_length=14)
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number", "password", "password2")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # fields = ("username","password")
