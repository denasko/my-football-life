from datetime import date, time, datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Event, FootballField


class EventCreationForm(forms.ModelForm):
    title = forms.CharField(label='Название события')
    description = forms.CharField(label='Описание события', widget=forms.Textarea(
        attrs={'placeholder': 'Введите описание события'}))
    date = forms.DateField(label='Дата события', widget=forms.DateInput(
        attrs={'type': 'date', 'placeholder': 'Выберите дату события'}))
    start_time = forms.TimeField(label='Время начала игры', widget=forms.TimeInput(
        attrs={'type': 'time', 'placeholder': 'Выберите время начала игры'}))
    max_players = forms.IntegerField(label='Максимальное количество игроков', widget=forms.NumberInput(
        attrs={'placeholder': 'Введите максимальное количество игроков'}))
    football_field = forms.ModelChoiceField(label='Футбольное поле', queryset=FootballField.objects.all(),
                                            widget=forms.Select(attrs={'placeholder': 'Выберите поле'}))

    def clean_date(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get("date")
        if selected_date < date.today():
            raise ValidationError("Нельзя создать событие на прошедшую дату")
        return selected_date

    def clean_start_time(self):
        cleaned_data = super().clean()
        selected_time = cleaned_data.get("start_time")
        current_time = datetime.now().time()
        if selected_time < time(hour=8) or selected_time > time(hour=22):
            raise ValidationError("Время начала игры должно быть между 8:00 и 22:00")
        if selected_time < current_time:
            raise ValidationError("Нельзя установить время начала игры в прошлом")
        return selected_time

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'start_time', 'max_players', 'football_field']
