from django.db import models


class Championship(models.Model):
    name = models.CharField(max_length=100)
    emblem = models.URLField(null=True)
    preview = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Чемпионат"
        verbose_name_plural = "Чемпионаты"

    def __str__(self):
        return f'Championship: {self.name}'


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Клуб")
    short_name = models.CharField(max_length=50, verbose_name="Короткое название")
    crest_url = models.URLField(verbose_name="Ссылка на фото")
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='championships',
                                     verbose_name="Чемпионат")

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"

    def __str__(self):
        return f'Team: {self.name}'


class TeamStanding(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='standing')
    position = models.IntegerField(null=True, verbose_name="Позиция")
    played_games = models.IntegerField(null=True, verbose_name="Сыгранно матчей")
    wins = models.IntegerField(null=True, verbose_name="Победы")
    draws = models.IntegerField(null=True, verbose_name="Ничьи")
    losses = models.IntegerField(null=True, verbose_name="Поражения")
    points = models.IntegerField(null=True, verbose_name="Очки")
    goals_for = models.IntegerField(null=True, verbose_name="Голов забито")
    goals_against = models.IntegerField(null=True, verbose_name="Голов пропущенно")
    goal_difference = models.IntegerField(null=True, verbose_name="Разница мячей")

    class Meta:
        verbose_name = "Положение в таблице"
        verbose_name_plural = "Положения в таблице"

    def __str__(self):
        return f'TeamStanding: {self.team.name}'


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches',
                                  verbose_name="Домашняя команда")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches',
                                  verbose_name="Команда гостей")
    date = models.DateTimeField(verbose_name="Начало матча")
    status = models.CharField(max_length=20, verbose_name="Статус")
    matchday = models.IntegerField(verbose_name="Игровой день")
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches',
                               verbose_name="Победитель")
    home_goals = models.IntegerField(null=True, verbose_name="Голы домашней команды", default=0)
    away_goals = models.IntegerField(null=True, verbose_name="Голы гостевой команды", default=0)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='matches',
                                     verbose_name="Чемпионат")

    class Meta:
        verbose_name = "Ближайший матч"
        verbose_name_plural = "Ближайшие матчи"

    def __str__(self):
        return f'Match: {self.home_team} vs {self.away_team}'


class NextMatchPreview(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='next_match_previews',
                                     verbose_name="Чемпионат")
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='next_match_preview',
                                 verbose_name="Матч")
    preview_text = models.TextField(verbose_name="Превью")
    photo = models.URLField(verbose_name="фото")

    class Meta:
        verbose_name = "Превью матча"
        verbose_name_plural = "Превью матчей"

    def __str__(self):
        return f"{self.championship.name} - {self.match.home_team.name} vs {self.match.away_team.name} - Preview"
