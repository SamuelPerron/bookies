from django.contrib import admin

from games.models import (
    League,
    City,
    Team,
    Match,
)


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
