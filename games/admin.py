from django.contrib import admin

from django.contrib.admin.filters import RelatedOnlyFieldListFilter

from games.models import (
    League,
    City,
    Team,
    Match,
)


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    template = 'admin/dropdown_filter.html'


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
    list_filter = (
        ('away_team', RelatedOnlyDropdownFilter),
        ('home_team', RelatedOnlyDropdownFilter),
        ('league', RelatedOnlyDropdownFilter)
    )
