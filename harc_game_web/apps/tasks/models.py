from chunked_upload.models import ChunkedUpload
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from apps.users.models import FreeDay, HarcgameUser, Scout

ChunkedFileUpload = ChunkedUpload


class UploadedFile(models.Model):
    """
    Model załadowanego pliku
    """
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    file = models.FileField()
    filename_orig = models.CharField(max_length=200, null=True)
    upload_id = models.CharField(max_length=32, null=True)

    def __str__(self):
        return f"{self.file.name} - {self.filename_orig} - {self.upload_id}"


class Task(models.Model):
    """
    Model zadania
    """
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    allowed_completition_frequency = models.CharField(max_length=200)
    prize = models.IntegerField(default=0, null=True)
    extra_prize = models.CharField(max_length=200, default=None, null=True)

    def __str__(self):
        return self.name


class DocumentedTask(models.Model):
    """
    Model udokumentowanego wykonanego zadania
    """
    task = models.ForeignKey(Task, on_delete=models.RESTRICT, null=True, default=None, related_name='documented_tasks')
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    date_completed = models.DateTimeField(default=timezone.now)
    comment_from_user = models.TextField(max_length=400, null=True, default="", blank=True)
    file1 = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, null=True, default=None, related_name='file1')
    file2 = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, null=True, default=None, related_name='file2')
    file3 = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, null=True, default=None, related_name='file3')
    link1 = models.CharField(max_length=400, null=True, default="", blank=True)
    link2 = models.CharField(max_length=400, null=True, default="", blank=True)
    link3 = models.CharField(max_length=400, null=True, default="", blank=True)

    def __str__(self):
        return f'{self.task} - completed by {self.user}'


class TaskApproval(models.Model):
    """
    Model zatwierdzania zadania (jako dodatkowe atrybuty udokumentowanego wykonania zadania
    """
    documented_task = models.OneToOneField(DocumentedTask, on_delete=models.CASCADE, related_name='task_approval')
    approver = models.ForeignKey(
        HarcgameUser, on_delete=models.RESTRICT, null=True, default=None
    )
    is_accepted = models.BooleanField(default=False)
    comment_from_approver = models.TextField(max_length=400, default="", blank=True)

    def __str__(self):
        return f'{self.documented_task} - approval by {self.approver}'


def pick_approver(user):
    """
    Function to pick TaskApprover to new task
    """
    user = Scout.objects.get(user=user)

    # get approvers that are in different team and do not have free day
    not_available_approvers = [free_day.user for free_day in FreeDay.objects.filter(day=timezone.now())]
    available_approvers = [
        t.user for t in
        Scout.objects.filter(is_team_leader=True).exclude(team=user.team).exclude(user__in=not_available_approvers)
    ]

    # pick one with least tasks to approve
    task_approval_count = {approver.id: 0 for approver in available_approvers}
    for task_approval in TaskApproval.objects.filter(approver__in=available_approvers).values():
        task_approval_count[task_approval['approver_id']] += 1

    return HarcgameUser.objects.get(id=min(task_approval_count, key=task_approval_count.get))


# @receiver(models.signals.post_save, sender=DocumentedTask)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         TaskApproval.objects.create(
#             documented_task=instance,
#             approver=pick_approver(instance.user)
#         )
#     instance.taskapproval.save()
