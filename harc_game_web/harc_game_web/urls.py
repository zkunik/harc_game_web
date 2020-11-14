"""
harc_game_web URL Configuration
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from apps.core.views import frontpage
from apps.tasks.views import UploadView, UploadCompleteView, complete_task
from apps.users.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('upload/', complete_task, name='upload'),
    path('api_upload/', UploadView.as_view(), name='api_upload'),
    path('api_upload_complete/', UploadCompleteView.as_view(), name='api_upload_complete')
]
