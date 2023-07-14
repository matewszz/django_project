from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'email', 'placeholder': 'Digite seu email'}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite sua senha'}
        )
    )
