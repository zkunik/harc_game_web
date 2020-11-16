from chunked_upload.constants import http_status, COMPLETE
from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.response import Response
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone

from apps.tasks.models import ChunkedFileUpload, DocumentedTask, UploadedFile
from apps.users.models import HarcgameUser, Scout, FreeDay


class CompleteTaskForm(forms.ModelForm):
    class Meta:
        model = DocumentedTask
        fields = ['task', 'comment_from_user', 'link1', 'link2', 'link3']


def pick_approver(user):
    """
    Function to pick TaskApprover to new task
    """
    # get approvers that are in different team
    # pick only those that do not have free day
    # pick one with least tasks
    user = Scout.objects.get(user=user)
    print(user)
    tl = Scout.objects.filter(is_team_leader=True)
    print(tl)
    tl = tl.exclude(team=user.team)
    print(tl)

    today_free_days = FreeDay.objects.filter(day=timezone.now())
    not_available_approvers = [free_day.user for free_day in today_free_days]

    tl = tl.exclude(user__in=not_available_approvers)
    print(tl)

    return 1


@login_required
def complete_task(request):
    """
    Function to handle completing Task by Scout - render and process form
    """
    if request.method == "POST":
        form = CompleteTaskForm(request.POST)

        if form.is_valid():
            documented_task = form.save()
            documented_task.user = request.user

            uploaded_files = []
            for upload_id_field in ['uploaded_file_info1', 'uploaded_file_info2', 'uploaded_file_info3']:
                upload_id = request.POST[upload_id_field]
                if upload_id != '':
                    file = UploadedFile.objects.filter(user=request.user, upload_id=upload_id).first()
                else:
                    file = None
                uploaded_files.append(file)
            documented_task.file1 = uploaded_files[0]
            documented_task.file2 = uploaded_files[1]
            documented_task.file3 = uploaded_files[2]

            approver_id = pick_approver(request.user)

            documented_task.save()

    else:
        form = CompleteTaskForm()
    completed_tasks = DocumentedTask.objects.filter(user=request.user)
    return render(request, 'tasks/upload.html', {'form': form, 'completed_tasks': completed_tasks})


class UploadView(ChunkedUploadView, LoginRequiredMixin):
    model = ChunkedFileUpload
    field_name = 'uploaded_file'

    def get(self, request):
        return redirect(reverse('upload'))


class UploadCompleteView(ChunkedUploadCompleteView, LoginRequiredMixin):
    model = ChunkedFileUpload

    def get(self, request):
        return redirect(reverse('upload'))

    def _post(self, request, *args, **kwargs):
        upload_id = request.POST.get('upload_id')
        md5 = request.POST.get('md5')

        error_msg = None
        if self.do_md5_check:
            if not upload_id or not md5:
                error_msg = "Both 'upload_id' and 'md5' are required"
        elif not upload_id:
            error_msg = "'upload_id' is required"
        if error_msg:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail=error_msg)

        chunked_upload = get_object_or_404(self.get_queryset(request),
                                           upload_id=upload_id)

        self.validate(request)
        self.is_valid_chunked_upload(chunked_upload)
        if self.do_md5_check:
            self.md5_check(chunked_upload, md5)

        chunked_upload.status = COMPLETE
        chunked_upload.completed_on = timezone.now()
        self._save(chunked_upload)
        self.on_completion(chunked_upload, request)

        return Response(self.get_response_data(chunked_upload, request),
                        status=http_status.HTTP_200_OK)

    def on_completion(self, chunked_upload, request):
        uploaded_file = chunked_upload.get_uploaded_file()
        UploadedFile.objects.create(
            user=request.user,
            file=uploaded_file,
            filename_orig=uploaded_file.name,
            upload_id=chunked_upload.upload_id
        )

    def get_response_data(self, chunked_upload, request):
        return {
            'filename': str(chunked_upload.filename),
            'upload_id': str(chunked_upload.upload_id),
        }
