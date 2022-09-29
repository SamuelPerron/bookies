from django.db import models


class Bookie(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def _get_source(self):
        source = None

        if self.name.lower().strip() == 'bet99':
            from odds.sources.bet99 import BET99
            source = BET99

        return source

    def import_data(self):
        source = self._get_source() 

        if source is None:
            raise AttributeError

        source().import_data(self)

    def get_details_path(self, external_id, league, sport):
        source = self._get_source()

        return source().get_details_path(external_id, league, sport)

    def __str__(self):
        return self.name


class Odds(models.Model):
    bookie = models.ForeignKey('odds.Bookie', on_delete=models.CASCADE, related_name='odds_set')
    match = models.ForeignKey('games.Match', on_delete=models.CASCADE, related_name='odds_set')

    away_odds = models.FloatField(blank=True, null=True)
    home_odds = models.FloatField(blank=True, null=True)

    us_away_odds = models.CharField(max_length=5, blank=True, null=True)
    us_home_odds = models.CharField(max_length=5, blank=True, null=True)

    refreshed_at = models.DateTimeField(null=True)
    external_id = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)

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

    def _convert_odds_on_save(self):
        if self.us_away_odds and not self.away_odds:
            self.away_odds = self._convert_us_to_decimal(self.us_away_odds)

        if self.us_home_odds and not self.home_odds:
            self.home_odds = self._convert_us_to_decimal(self.us_home_odds)

        self.us_home_odds = None
        self.us_away_odds = None

    def _build_url_on_save(self):
        if not self.url:
            self.url = self.bookie.get_details_path(
                self.external_id,
                self.match.league.name.lower(),
                self.match.league.sport.lower()
            )

    def save(self, *args, **kwargs):
        # US odds
        self._convert_odds_on_save()

        # Build url
        self._build_url_on_save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.match} | {self.away_odds} - {self.home_odds}'

    class Meta:
        verbose_name_plural = 'Odds'
