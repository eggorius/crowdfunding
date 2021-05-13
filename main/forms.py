from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'firstName',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'lastName',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class LoginForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} does not exist.')
        user = User.objects.get(username=username)
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Wrong password')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_username',
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'id_password',
                'placeholder': 'Password'
            }),
        }




