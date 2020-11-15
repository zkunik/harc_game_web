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
    Model udokumentowanego zadania (wykonanego)
    """
    task = models.ForeignKey(Task, on_delete=models.RESTRICT, null=True, default=None)
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None, related_name='user')
    date_completed = models.DateTimeField(default=timezone.now)
    comment_from_user = models.TextField(max_length=400, null=True, default="", blank=True)
    file1 = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, null=True, default=None, related_name='file1')
    file2 = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, null=True, default=None, related_name='file2')
    file3 = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, null=True, default=None, related_name='file3')
    link1 = models.CharField(max_length=400, null=True, default="", blank=True)
    link2 = models.CharField(max_length=400, null=True, default="", blank=True)
    link3 = models.CharField(max_length=400, null=True, default="", blank=True)

    approver = models.ForeignKey(
        HarcgameUser, on_delete=models.RESTRICT, null=True, default=None, related_name='approver'
    )
    is_accepted = models.BooleanField(default=False)
    comment_from_approver = models.TextField(max_length=400)

    def __str__(self):
        return f'{self.task} - completed by {self.user}'
