from django.contrib import admin

from .models import Team, TeamStanding, Championship, Match


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'get_championship')
    list_filter = ('championship',)
    search_fields = ('name', 'short_name')

    def get_championship(self, obj):
        return obj.championship.name

    get_championship.short_description = 'Championship'


class TeamStandingAdmin(admin.ModelAdmin):
    list_display = (
    'team', 'position', 'points', 'played_games', 'wins', 'draws', 'losses', 'goals_for', 'goals_against',
    'goal_difference', 'get_championship')
    list_filter = ('team__championship',)
    search_fields = ('team__name',)

    def get_championship(self, obj):
        return obj.team.championship.name

    get_championship.short_description = 'Championship'


class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'date', 'status', 'matchday', 'winner', 'home_goals', 'away_goals', 'championship']
    list_filter = ['status', 'matchday', 'championship']
    search_fields = ['home_team__name', 'away_team__name', 'date']
    date_hierarchy = 'date'



admin.site.register(Team, TeamAdmin)
admin.site.register(TeamStanding, TeamStandingAdmin)
admin.site.register(Championship, ChampionshipAdmin)
