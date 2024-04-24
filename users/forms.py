from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .models import Profile, Feedback

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
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Проверка на уникальность email адреса
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email адресом уже существует')

        return email

# _______________________________________________Profile___________________________________________________


class CustomUserForm(UserChangeForm):
    birthday = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(1940, 2023)))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday']


class RefactorProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}))
    bio = forms.CharField(label='Расскажите о себе', widget=forms.Textarea(attrs={'placeholder': 'Где играете, за какой клуб болеете и тп.'}))

    class Meta:
        model = Profile
        fields = ['phone_number', 'bio']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number is not None and len(phone_number) != 13:
            self.add_error('phone_number', 'Введите корректный номер телефона')

        return phone_number


# _______________________________________________Feedback___________________________________________________
class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Оценка сайта')
    header = forms.CharField(label='Заголовок', widget=forms.TextInput(
        attrs={'placeholder': 'Введите заголовок сообщения'}))
    comment = forms.CharField(label='Ваш комментарий', widget=forms.Textarea)

    class Meta:
        model = Feedback
        fields = ['rating', 'header', 'comment']