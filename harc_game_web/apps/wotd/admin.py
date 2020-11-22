from django.contrib import admin

from apps.wotd.models import WordOfTheDay


@admin.register(WordOfTheDay)
class EventAdmin(admin.ModelAdmin):
    fields = ('question', 'hint', 'answer', 'date')
    list_display = ('date',)
    list_filter = ('date',)
    search_fields = ('question', 'answer')
    ordering = ('date',)