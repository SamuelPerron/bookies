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

    @property
    def arbitrage_pairs(self):
        multi_array = []
        values = self.odds_set.all().values(
            'id', 'away_odds', 'home_odds'
        )
        profitable_odds = []

        for i, odds in enumerate(values):
            for j in range(2):
                for other_odds in values[i:]:
                    if j == 0:
                        calculation = 1 / odds['away_odds'] + 1 / other_odds['home_odds']
                    else:
                        calculation = 1 / odds['home_odds'] + 1 / other_odds['away_odds']

                    multi_array.append(
                        (odds['id'], other_odds['id'], j, calculation)
                    )

        for odds in multi_array:
            if odds[3] < 1:
                profitable_odds.append(odds)

        return profitable_odds

    @property
    def arbitrage_possibility(self):
        return bool(len(self.arbitrage_pairs))


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

    away_odds = models.FloatField(blank=True, null=True)
    home_odds = models.FloatField(blank=True, null=True)

    us_away_odds = models.CharField(max_length=5, blank=True, null=True)
    us_home_odds = models.CharField(max_length=5, blank=True, null=True)

    @property
    def implied_probability(self):
        if not self.away_odds or not self.home_odds:
            return None

        probability = 1 / self.away_odds + 1 / self.home_odds
        return f'{round(probability * 100, 2)} %'

    def _convert_us_to_decimal(self, us_odds):
        if us_odds[0] == '+':
            return self.us_away_odds / 100 + 1

        return 100 / self.us_away_odds + 1

    def save(self, *args, **kwargs):
        if self.us_away_odds and not self.away_odds:
            self.away_odds = self._convert_us_to_decimal(self.us_away_odds)

        if self.us_home_odds and not self.home_odds:
            self.home_odds = self._convert_us_to_decimal(self.us_home_odds)

        self.us_home_odds = None
        self.us_away_odds = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.match} | {self.away_odds} - {self.home_odds}'

    class Meta:
        verbose_name_plural = 'Odds'
