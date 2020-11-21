from django.contrib import admin

from apps.tasks.models import Task, DocumentedTask, TaskApproval

admin.site.register(Task)
admin.site.register(DocumentedTask)
admin.site.register(TaskApproval)
