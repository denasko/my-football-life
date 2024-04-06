from django.contrib import admin

from .models import Team, TeamStanding, Championship


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'championship')
    list_filter = ('championship',)
    search_fields = ('name', 'short_name')


class TeamStandingAdmin(admin.ModelAdmin):
    list_display = (
    'team', 'position', 'points', 'played_games', 'wins', 'draws', 'losses', 'goals_for', 'goals_against',
    'goal_difference')
    list_filter = ('team__championship',)
    search_fields = ('team__name',)


class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamStanding, TeamStandingAdmin)
admin.site.register(Championship, ChampionshipAdmin)
