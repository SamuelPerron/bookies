from django.contrib import admin

from odds.models import (
    Bookie, 
    League,
    City,
    Team,
    Match,
    Odds
)


admin.site.register(Bookie)
admin.site.register(League)
admin.site.register(City)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Odds)
