from django.contrib import admin

from apps.posts.models import Post

@admin.register(Post)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
       (None, {'fields': ('title', 'content', 'pub_date_time', 'user')}),
       ('Optional Information', {
            'description': 'Dodatkowe dane',
            'classes': ('collapse',),
            'fields': ('link1', 'link2', 'link3', 'date_time')
       }),
   )
    list_display = ('pub_date_time', 'title', 'user')
    list_filter = ('user', 'pub_date_time')
    search_fields = ('title', 'content', 'link1', 'link2', 'link3')
    ordering = ('-pub_date_time',)