from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text'})
    )
    password = forms.CharField(
        help_text="Password must be combination of alphabets and numbers",
        widget=forms.PasswordInput(attrs={'type': 'password'})
    )
    # RegEx
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text'})
    )

    def clean(self, args, **kwargs):
        print("1")
        username = self.cleaned_data.get('username')
        # check if username already exists
        username_qs = User.objects.get(Q(username=username))
        if username_qs.exists():
            raise forms.ValidationError(_("Sorry! User with this username already exists. Try with another username."))
        # return username

        email = self.cleaned_data.get('email')
        # check if email already exists
        email_qs = User.objects.get(Q(email=email))
        if email_qs.exists():
            raise forms.ValidationError(_("Sorry! User with this email already exists. Try with another email."))
        # return email

        return super(RegistrationForm, self).clean(*args, **kwargs)
    #
    # def clean_email(self):
    #     print("2")
    #     email = self.cleaned_data.get('email')
    #     # check if email already exists
    #     email_qs = User.objects.get(Q(email=email))
    #     if email_qs.exists():
    #         raise forms.ValidationError(_("Sorry! User with this email already exists. Try with another email."))
    #     return email
