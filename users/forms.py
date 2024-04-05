from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import re
from .models import Profile

# _______________________________________________Registration___________________________________________________


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}),
                             validators=[EmailValidator(message='Введите корректный email адрес')])
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'Повторите ваш пароль'}))

    def clean_password(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Проверка на уникальность email адреса
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email адресом уже существует')

        return email

# _______________________________________________Profile___________________________________________________


class RefactorProfileForm(forms.ModelForm):
    birthday = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(1940, 2023)))

    class Meta:
        model = Profile
        fields = ['birthday', 'phone_number', 'bio']
        labels = {
            'phone_number': 'Номер телефона',
            'bio': 'Расскажите о себе'
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Где играете, за какой клуб болеете и тп.'})
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number is not None and len(phone_number) != 13:
            self.add_error('phone_number', 'Введите корректный номер телефона')

        return phone_number

