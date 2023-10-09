from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
# from allauth.account.forms import SignupForm
from django.utils.translation import gettext as _

from .models import User


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