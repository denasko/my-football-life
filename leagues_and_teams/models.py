from django.db import models


class Championship(models.Model):
    name = models.CharField(max_length=100)
    emblem = models.URLField(null=True)

    def __str__(self):
        return f'Championship: {self.name}'


class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    crest_url = models.URLField()
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='championships')

    def __str__(self):
        return f'Team: {self.name}'

class TeamStanding(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='standing')
    position = models.IntegerField(null=True)
    played_games = models.IntegerField(null=True)
    wins = models.IntegerField(null=True)
    draws = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    goals_for = models.IntegerField(null=True)
    goals_against = models.IntegerField(null=True)
    goal_difference = models.IntegerField(null=True)

    def __str__(self):
        return f'TeamStanding: {self.team.name}'




