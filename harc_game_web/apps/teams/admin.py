from django.contrib import admin

from apps.teams.models import Team, Patrol

@admin.register(Team)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name', 'colors', 'tax')
    list_display = ('name', 'short_name', 'colors', 'tax')
    list_filter = ('tax',)

@admin.register(Patrol)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'team')
    list_display = ('name', 'team')
    list_filter = ('team',)
