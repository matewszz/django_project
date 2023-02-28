from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    Confirmar_Senha = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Favor, confirme a senha!'
        })
    )

    class Meta:
        model = User                     ##
        fields = [                       # campos que terá para o usuario imputar dados #
            'first_name',                ##
            'last_name',                 ##
            'username',
            'email',
            'password',
            
        ]

        widgets = {     # Serve para sobrescrever o campo#
            'password': forms.PasswordInput(attrs={ # esconde o imput da senha #
                'placeholder': 'Digite sua senha, por favor!' # Texto que fica dentro do imput #
            })   
        }

