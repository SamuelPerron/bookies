from django.contrib import admin

from odds.models import Bookie, Odds


@admin.register(Bookie)
class BookieAdmin(admin.ModelAdmin):
    actions = ('import_data',)

    @admin.action(description='Import data')
    def import_data(self, request, queryset):
        for bookie in queryset:
            bookie.import_data()


@admin.register(Odds)
class OddsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('bookie', 'match', 'refreshed_at', 'external_id', 'url')
        }),
        ('Odds', {
            'fields': ('away_odds', 'home_odds', 'us_away_odds', 'us_home_odds')
        }),
        ('Calculations', {
            'fields': ('implied_probability',)
        }),
    )

    readonly_fields = ('implied_probability', 'external_id', 'url')
    writeonly_fields = ('us_away_odds', 'us_home_odds')

    list_display = (
        'bookie',
        'match',
        'away_odds',
        'home_odds'
    )
