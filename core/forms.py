from django import forms
from . import models
from django.contrib.auth.models import User
import re


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'User Name',
            'password': 'Password',
            'confirm_password': 'Confirm password',
        }
    
    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")

        if User.objects.filter(email=email):
            self.add_error('email', "This email already registered.")

        if User.objects.filter(username=username):
            self.add_error('username', "This username is already registered.")

        if password != confirm_password:
            self.add_error("confirm_password", "passwords do not match.")

class ProfileCreateForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=models.Role.objects.all(), label='Role', required=True)

    class Meta:
        model = models.Profile
        fields = ('role', 'country', 'mobile')
        labels = {
            'role': 'Role',
            'country': 'country',
            'mobile': 'mobile',
        }
    def clean(self):
        cleaned_data = super(ProfileCreateForm, self).clean()
        mobile = cleaned_data.get('mobile')
        regnum = r'^([0-9]{10})$'
        try:
            obj2 = re.match(regnum, mobile)
            if obj2:
                pass
            else:
                self.add_error('mobile', "Please enter valid number")
        except:
            self.add_error('mobile', "Please enter valid number")
    
    def __init__(self, user, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
