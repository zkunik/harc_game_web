from django.contrib import admin

from apps.tasks.models import Task, DocumentedTask, TaskApproval


@admin.register(Task)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'category','description',
              'allowed_completition_frequency', ('prize', 'extra_prize'))
    list_display = ('name', 'category', 'allowed_completition_frequency', 'prize', 'extra_prize')
    list_filter = ('category', 'allowed_completition_frequency', 'extra_prize', 'prize')
    ordering = ('name',)

@admin.register(DocumentedTask)
class EventAdmin(admin.ModelAdmin):
    fields = ('task', 'user', 'date_completed', 'comment_from_user',
        'file1', 'file2', 'file3', 'link1', 'link2', 'link3')
    list_display = ('task', 'user', 'date_completed')
    list_filter = ('user', 'date_completed', 'task')

@admin.register(TaskApproval)
class EventAdmin(admin.ModelAdmin):
    fields = ('documented_task', 'approver','is_accepted', 'comment_from_approver')
    list_display = ('documented_task', 'approver', 'is_accepted')
    list_filter = ('is_accepted', 'approver', 'documented_task')
