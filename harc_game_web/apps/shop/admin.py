from django.contrib import admin

from apps.shop.models import Request, Vote, Item, ItemOffer


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


@admin.register(Item)
class EventAdmin(admin.ModelAdmin):
    fields = ('name_pl', 'name_eng', 'category', 'link_image', 'description')
    list_display = ('name_pl', 'name_eng', 'category')
    list_filter = ('name_pl', 'name_eng', 'category')


@admin.register(ItemOffer)
class EventAdmin(admin.ModelAdmin):
    fields = ('item', 'price', 'is_available')
    list_display = ('item', 'price', 'is_available')
    list_filter = ('item', 'price', 'is_available')
