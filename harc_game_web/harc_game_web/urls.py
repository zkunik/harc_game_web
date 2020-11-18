"""
harc_game_web URL Configuration
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path


from apps.core.views import frontpage
from apps.tasks.views import UploadView, UploadCompleteView, complete_task
from apps.users.views import signup
from apps.posts.views import list_active_posts, list_all_posts, view_post, edit_post, new_post, delete_post
from apps.teams.views import TeamForm


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', frontpage, name='frontpage'),
    path('', list_active_posts, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),

    path('upload/', complete_task, name='upload'),
    path('api_upload/', UploadView.as_view(), name='api_upload'),
    path('api_upload_complete/', UploadCompleteView.as_view(), name='api_upload_complete'),

    # Posts

    path('posts/', list_active_posts, name='all_posts_hp'),
    path('posts/list/', list_all_posts, name='all_posts'),
    path('posts/view/<slug:slug>', view_post, name='view_post'),
    path('posts/new/', new_post, name='new_post'),
    path('posts/edit/<slug:slug>', edit_post, name='edit_post'),
    path('posts/delete/<slug:slug>', delete_post, name='delete_post'),

    # Teams
    path('teams/list/', TeamForm.list, name='all_teams'),
    path('teams/view/<slug:id>', TeamForm.view, name='view_team'),

]
