from django.contrib import admin

from .models import Team, TeamStanding, Championship, Match, NextMatchPreview


class NextMatchPreviewInline(admin.StackedInline):
    model = NextMatchPreview
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'get_championship')
    list_filter = ('championship',)
    search_fields = ('name', 'short_name')
    list_per_page = 20

    def get_championship(self, obj):
        return obj.championship.name

    get_championship.short_description = 'Championship'


@admin.register(TeamStanding)
class TeamStandingAdmin(admin.ModelAdmin):
    list_display = (
        'team', 'position', 'points', 'played_games', 'wins', 'draws', 'losses', 'goals_for', 'goals_against',
        'goal_difference', 'get_championship')
    list_filter = ('team__championship',)
    search_fields = ('team__name',)
    list_per_page = 20

    def get_championship(self, obj):
        return obj.team.championship.name

    get_championship.short_description = 'Championship'


@admin.register(Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'date', 'status', 'matchday', 'winner', 'home_goals', 'away_goals',
                    'championship']
    list_filter = ['status', 'matchday', 'championship']
    search_fields = ['home_team__name', 'away_team__name', 'date']
    date_hierarchy = 'date'
    list_per_page = 10
    inlines = [NextMatchPreviewInline]


@admin.register(NextMatchPreview)
class NextMatchPreviewAdmin(admin.ModelAdmin):
    list_display = ['championship', 'match', 'preview_text']
    list_filter = ['championship']
    search_fields = ['championship__name', 'match__home_team__name', 'match__away_team__name']
    list_per_page = 10
