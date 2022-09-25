from django.contrib import admin

from odds.models import Bookie, Odds


admin.site.register(Bookie)


@admin.register(Odds)
class OddsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('bookie', 'match')
        }),
        ('Odds', {
            'fields': ('away_odds', 'home_odds', 'us_away_odds', 'us_home_odds')
        }),
        ('Calculations', {
            'fields': ('implied_probability',)
        }),
    )

    readonly_fields = ('implied_probability',)
    writeonly_fields = ('us_away_odds', 'us_home_odds')

    list_display = (
        'bookie',
        'match',
        'away_odds',
        'home_odds'
    )
