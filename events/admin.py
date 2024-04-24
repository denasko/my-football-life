from django.contrib import admin

from .models import FootballField, Event, Players


class FootballFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'football_field', 'date', 'max_players')
    filter_horizontal = ('players',)


class PlayersAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status')
    list_filter = ('event', 'status')


admin.site.register(FootballField, FootballFieldAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Players, PlayersAdmin)
