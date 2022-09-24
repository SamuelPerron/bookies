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


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('date', 'league', 'away_team', 'home_team')
        }),
        ('Calculations', {
            'fields': ('arbitrage_pairs',)
        }),
    )

    readonly_fields = ('arbitrage_pairs',)

    list_display = (
        'date',
        'league',
        'away_team',
        'home_team',
        'arbitrage_possibility'
    )


@admin.register(Odds)
class OddsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('bookie', 'match')
        }),
        ('Odds', {
            'fields': ('away_odds', 'home_odds')
        }),
        ('Calculations', {
            'fields': ('implied_probability',)
        }),
    )

    readonly_fields = ('implied_probability',)

    list_display = (
        'bookie',
        'match',
        'away_odds',
        'home_odds'
    )
