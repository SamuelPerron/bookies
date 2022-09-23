from django.db import models
from django.utils import timezone


class Bookie(models.Model):
    name = models.CharField(blank=False, max_length=255)
    base_url = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.CharField(blank=False, max_length=4)
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return f'({self.country}) {self.name}'

    class Meta:
        verbose_name_plural = 'Cities'


class Team(models.Model):
    league = models.ForeignKey('odds.League', on_delete=models.CASCADE, related_name='team_set')
    city = models.ForeignKey('odds.City', on_delete=models.CASCADE, related_name='team_set')
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return f'{self.city} {self.name}'


class Match(models.Model):
    date = models.DateTimeField()

    league = models.ForeignKey('odds.League', on_delete=models.CASCADE, related_name='match_set')
    away_team = models.ForeignKey('odds.Team', on_delete=models.CASCADE, related_name='away_match_set')
    home_team = models.ForeignKey('odds.Team', on_delete=models.CASCADE, related_name='home_match_set')

    def __str__(self):
        date = timezone.localtime(
            self.date, 
            timezone.get_default_timezone()
        ).strftime("%d %b - %H:%M")

        return f'{date} | {self.league} | {self.away_team} vs {self.home_team}'

    class Meta:
        verbose_name_plural = 'Matches'

    
class Odds(models.Model):
    bookie = models.ForeignKey('odds.Bookie', on_delete=models.CASCADE, related_name='odds_set')
    match = models.ForeignKey('odds.Match', on_delete=models.CASCADE, related_name='odds_set')

    away_odds = models.FloatField(blank=False)
    home_odds = models.FloatField(blank=False)

    def __str__(self):
        return f'{self.match} | {self.away_odds} - {self.home_odds}'

    class Meta:
        verbose_name_plural = 'Odds'
