from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.shortcuts import render, redirect
from django import forms

from apps.tasks.models import FileUpload, DocumentedTask


class CompleteTaskForm(forms.ModelForm):
    class Meta:
        model = DocumentedTask
        fields = ['task', 'comment_from_user', 'link1', 'link2', 'link3']


def complete_task(request):
    """
    Function to handle completing Task by Scout - render and process form
    """
    if request.method == "POST":
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
    model = FileUpload
    field_name = 'uploaded_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class UploadCompleteView(ChunkedUploadCompleteView):
    model = FileUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.file)

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}
