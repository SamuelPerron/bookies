from django.utils import timezone
from datetime import datetime
from odds.models import Odds

from odds.sources import Source
from games.models import League, City, Team, Match


class BET99(Source):
    base_url = 'https://bet99.com/en/'
    obj = None

    def _fetch_events(self, data):
        return data['Result']['Items'][0]['Events']
        

    def import_data(self, obj):
        self.obj = obj
        now = timezone.now()
        data = self._fetch_url(
            'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=240&langId=8&skinName=bet99&configId=17&culture=en-GB&countryCode=CA&deviceType=Desktop&numformat=en&integration=bet99&sportids=0&categoryids=0&champids=3281&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&startDate=2022-09-25T23%3A37%3A00.000Z&endDate=2022-10-02T23%3A37%3A00.000Z'
        )

        events = self._fetch_events(data.json())

        for event in events:
            league, _ = League.objects.get_or_create(
                name=event['ChampName']
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
                )
                money_line = event['Items'][0]['Items']
                odds.away_odds = money_line[0]['Price']
                odds.home_odds = money_line[1]['Price']
                odds.save()

    
