from django.contrib import admin

from apps.shop.models import Request, Vote

@admin.register(Request)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
       (None, {'fields': ('user', 'content', 'price', 'date')}),
       ('Optional Information', {
            'description': 'Dodatkowe dane',
            'classes': ('collapse',),
            'fields': ('link1', 'link2', 'link3')
       }),
    )
    list_display = ('user', 'content', 'price', 'date')
    list_filter = ('user', 'date', 'price')
    search_fields = ('content', 'link1', 'link2', 'link3')
    ordering = ('date',)

@admin.register(Vote)
class EventAdmin(admin.ModelAdmin):
    fields = ('user', 'request')
    list_display = ('user', 'request')
    list_filter = ('user', 'request')
