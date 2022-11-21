from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User                     ##
        fields = [                       # campos que terá para o usuario imputar dados #
            'first_name',                ##
            'last_name',                 ##
            'username',
            'email',
            'password',
        ]