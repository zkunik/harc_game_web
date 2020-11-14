from django.views.generic.base import TemplateView
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from apps.tasks.models import FileUpload
from django.shortcuts import render


class UploadPage(TemplateView):
    template_name = 'tasks/upload.html'


def complete_task(request):
    """
    Function to handle completing Task by Scout - render and process form
    """
    return render(request, 'tasks/upload.html')


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
