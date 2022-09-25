from django.db import models


class Bookie(models.Model):
    name = models.CharField(blank=False, max_length=255)
    base_url = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class Odds(models.Model):
    bookie = models.ForeignKey('odds.Bookie', on_delete=models.CASCADE, related_name='odds_set')
    match = models.ForeignKey('games.Match', on_delete=models.CASCADE, related_name='odds_set')

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
