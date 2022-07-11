from django import forms
#


class NewLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', max_length=10)
