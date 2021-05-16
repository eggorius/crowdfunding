from django import forms
from django.contrib.auth.models import User
from .models import Company, Rating, RatingStar, Photo, Comment


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'User with such email already exists.')
        return email


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


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['title', 'description', 'video_url', 'theme', 'goal', 'date_finish']
        widgets = {
            'date_finish': forms.SelectDateWidget(),
        }


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(),
                                  widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ['star']


class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['title', 'description', 'video_url', 'theme', 'goal', 'date_finish']
        widgets = {
            'date_finish': forms.SelectDateWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']
