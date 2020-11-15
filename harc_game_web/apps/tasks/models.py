from chunked_upload.models import ChunkedUpload
from django.db import models
from django.utils import timezone
from apps.users.models import HarcgameUser

# 'ChunkedUpload' class provides almost everything for you.
# if you need to tweak it little further, create a model class
# by inheriting "chunked_upload.models.AbstractChunkedUpload" class
ChunkedFileUpload = ChunkedUpload


class UploadedFile(models.Model):
    """
    Model załadowanego pliku
    """
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    file = models.FileField()


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
    Model udokumentowanego zadania (wykonanego)
    """
    task = models.ForeignKey(Task, on_delete=models.RESTRICT, null=True, default=None)
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None, related_name='user')
    date_completed = models.DateTimeField(default=timezone.now)
    comment_from_user = models.TextField(max_length=400)
    filepath1 = models.CharField(max_length=200, null=True, default=None)
    filepath2 = models.CharField(max_length=200, null=True, default=None)
    filepath3 = models.CharField(max_length=200, null=True, default=None)
    link1 = models.CharField(max_length=400, null=True, default=None, blank=True)
    link2 = models.CharField(max_length=400, null=True, default=None, blank=True)
    link3 = models.CharField(max_length=400, null=True, default=None, blank=True)

    approver = models.ForeignKey(
        HarcgameUser, on_delete=models.RESTRICT, null=True, default=None, related_name='approver'
    )
    is_accepted = models.BooleanField(default=False)
    comment_from_approver = models.TextField(max_length=400)

    def __str__(self):
        return f'{self.task} - completed by {self.user}'
