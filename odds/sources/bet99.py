from django.utils import timezone
from datetime import datetime

from odds.models import Odds
from odds.sources import Source
from games.models import League, City, Team, Match


class BET99(Source):
    base_betting_url = 'https://bet99.com/en/sport-betting#'
    base_url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents'
    obj = None
    leagues = {
        'nfl': '3281',
        'nhl': '3232',
        'nba': '2980',
    }
    sports = {
        'football': '75',
        'hockey': '70',
        'basketball': '67',
    }
    event_types = {
        'default': '0'
    }

    def _fetch_events(self, data):
        return data['Result']['Items'][0]['Events']

    def _build_url(self, league):
        now = timezone.now()

        params = {
            'timezoneOffset': 240,
            'langId': 8,
            'skiyynName': 'bet99',
            'configId': 17,
            'culture': 'en-GB',
            'countryCode': 'CA',
            'deviceType': 'Desktop',
            'numformat': 'en',
            'integration': 'bet99',
            'sportids': 0,
            'categoryids': 0,
            'group': 'AllEvents',
            'period': 'periodall',
            'withLive': 'false',
            'outrightsDisplay': 'none',
            'marketTypeIds': '',
            'couponType': 0,
            'startDate': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'endDate': (
                now + timezone.timedelta(days=15)
            ).strftime('%Y-%m-%dT%H:%M:%SZ'),
        }

        params['champids'] = self.leagues[league]

        return self.base_url + self._params_to_url(params)
       
    def get_details_path(self, external_id, league, sport):
        sport_id = self.sports[sport]
        event_type = self.event_types['default']
        league_id = self.leagues[league]

        return f'{self.base_betting_url}/event/{sport_id}/{event_type}/{league_id}/all/{external_id}'

    def import_data(self, obj):
        self.obj = obj
        now = timezone.now()

        for league in self.leagues:
            data = self._fetch_url(
                self._build_url(league)
            )

            events = self._fetch_events(data.json())

            for event in events:
                league_name = event['ChampName'].strip()
                league, _ = League.objects.get_or_create(
                    name=league_name
                )

                teams = []
                for team in event['Competitors']:
                    team_name = team['Name'].strip().split(' ')

                    city, _ = City.objects.get_or_create(
                        country=event['ISO'],
                        name=team_name[0]
                    )
                    team, _ = Team.objects.get_or_create(
                        league_id=league.id,
                        city_id=city.id,
                        name=team_name[1]
                    )
                    teams.append(team)

                event_date = timezone.make_aware(datetime.strptime(
                    event['EventDate'],
                    '%Y-%m-%dT%H:%M:%SZ'
                ))
                if event_date > now:
                    match, _ = Match.objects.get_or_create(
                        date=event_date,
                        league_id=league.id,
                        away_team=teams[0],
                        home_team=teams[1]
                    )

                    odds, _ = Odds.objects.get_or_create(
                        bookie_id=self.obj.id,
                        match_id=match.id,
                        external_id=event['Id'],
                    )
                    money_line = event['Items'][0]['Items']
                    odds.away_odds = money_line[0]['Price']
                    odds.home_odds = money_line[1]['Price']
                    odds.refreshed_at = timezone.now()
                    odds.save()

