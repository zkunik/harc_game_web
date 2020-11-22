from django.contrib import admin

from apps.bank.models import Bank

@admin.register(Bank)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
       ('Required Information', {
            'description': "Proszę podać poniższe dane",
            'fields': ('user', 'date_accrued','documented_task',
                ('accrual', 'accrual_type', 'accrual_deleted'), 'accrual_extra_prize')
       }),
       ('Optional Information', {
            'description': "Dodatkowe dane",
            'classes': ('collapse',),
            'fields': ('year_week',)
       }),
   )
    list_display = ('date_accrued', 'user', 'documented_task', 'accrual_type', 'accrual_deleted')
    list_filter = ('user', 'date_accrued', 'accrual_type', 'accrual_deleted')
    ordering = ('-date_accrued',)