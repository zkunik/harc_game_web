from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.views import HarcgameUserCreationForm
from apps.users.models import HarcgameUser


class CustomUserAdmin(UserAdmin):
    add_form = HarcgameUserCreationForm
    model = HarcgameUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'nickname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'admin' 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(HarcgameUser, CustomUserAdmin)
