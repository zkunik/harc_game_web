from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView

from chunked_upload.response import Response
from chunked_upload.constants import http_status
from django import forms
from django.shortcuts import render

from apps.tasks.models import ChunkedFileUpload, DocumentedTask, UploadedFile


class CompleteTaskForm(forms.ModelForm):
    class Meta:
        model = DocumentedTask
        fields = ['task', 'comment_from_user', 'link1', 'link2', 'link3']


def complete_task(request):
    """
    Function to handle completing Task by Scout - render and process form
    """
    if request.method == "POST":
        print(f'request.POST: {request.POST}')
        form = CompleteTaskForm(request.POST)

        if form.is_valid():
            completed_task = form.save()
            completed_task.user = request.user
            completed_task.save()

    else:
        form = CompleteTaskForm()
    completed_tasks = DocumentedTask.objects.filter(user=request.user)
    return render(request, 'tasks/upload.html', {'form': form, 'completed_tasks': completed_tasks})


class UploadView(ChunkedUploadView):
    model = ChunkedFileUpload
    field_name = 'uploaded_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class UploadCompleteView(ChunkedUploadCompleteView):
    model = ChunkedFileUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        print(uploaded_file.name)
        print(uploaded_file.file)
        print()
        UploadedFile.objects.create(user=request.user, file=uploaded_file)

    def get_response_data(self, chunked_upload, request):
        return {
            'filename': str(chunked_upload.filename),
            'file': str(chunked_upload.file),
            'upload_id': str(chunked_upload.upload_id),
        }
