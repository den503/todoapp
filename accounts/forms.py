from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password_confirmation(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirmation']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password_confirmation']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'E-mail'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', )
        labels = {'birth_date': 'Дата рождения'}
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }
