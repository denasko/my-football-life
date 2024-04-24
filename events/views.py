from django.shortcuts import render, redirect

from events.forms import EventCreationForm
from .models import FootballField


def football_map(request):
    football_fields = FootballField.objects.all()
    return render(request, template_name='events/first.html', context={'football_fields': football_fields})


def football_field(request, football_field_name: FootballField.name):
    football_field: 'FootballField' = FootballField.objects.get(name=football_field_name)
    return render(request, template_name='events/football_field.html', context={'football_field': football_field})


def create_event(request, football_field_name: FootballField.name):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            date = form.cleaned_data.get('date')
            start_time = form.cleaned_data.get('start_time')
            max_players = form.cleaned_data.get('max_players')
            football_field = FootballField.objects.get(name=football_field_name)

            print(title, description, date, start_time, max_players, football_field, sep='\n')

            # event = form.save(commit=False)
            # event.save()
            return redirect('events:football_field', football_field_name=football_field_name)
    else:
        form = EventCreationForm()
    return render(request, template_name='events/create_event.html', context={'form': form})
