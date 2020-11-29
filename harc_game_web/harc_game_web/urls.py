"""
harc_game_web URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from apps.core.views import frontpage
from apps.tasks.views import UploadView, UploadCompleteView, add_completed_task, check_task, TaskView, \
    all_documented_tasks, list_completed_tasks, edit_completed_task, fav_task, unfav_task
from apps.users.views import signup
from apps.posts.views import list_active_posts, list_all_posts, view_post, edit_post, new_post, delete_post
from apps.teams.views import view_teams_list, view_team
from apps.wotd.views import WordOfTheDayView
from apps.bank.views import BankReport
from apps.tasks.scheduler import start_scheduler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),

    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),

    # tasks
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('completed_tasks/<str:tab>'', list_completed_tasks, name='list_completed_tasks'),
    path('completed_tasks/new/', add_completed_task, name='add_completed_task'),
    path('completed_tasks/edit/<slug:documented_task_id>', edit_completed_task, name='edit_completed_task'),
    path('completed_tasks/fav/<int:id>', fav_task, name='fav_task'),
    path('completed_tasks/fav/<int:id>/<str:tab>', fav_task, name='fav_task'),
    path('completed_tasks/unfav/<int:id>', unfav_task, name='unfav_task'),
    path('completed_tasks/unfav/<int:id>/<str:tab>', unfav_task, name='unfav_task'),
    path('check_task/', check_task, name='check_task'),
    path('all_documented_tasks/', all_documented_tasks, name='all_documented_tasks'),
    path('api_upload/', UploadView.as_view(), name='api_upload'),
    path('api_upload_complete/', UploadCompleteView.as_view(), name='api_upload_complete'),

    # Posts
    path('posts/', list_active_posts, name='all_posts'),
    path('posts/edit/', list_all_posts, name='edit_posts'),
    path('posts/view/<slug:slug>', view_post, name='view_post'),
    path('posts/new/', new_post, name='new_post'),
    path('posts/edit/<slug:slug>', edit_post, name='edit_post'),
    path('posts/delete/<slug:slug>', delete_post, name='delete_post'),

    # Teams
    path('teams/list/', view_teams_list, name='all_teams'),
    path('teams/view/<slug:team_id>', view_team, name='view_team'),

    # WordOfTheDay
    path('wotd/', WordOfTheDayView.as_view(), name='word_of_the_day'),

    # Bank & reporting
    path('report/', staff_member_required(BankReport.as_view()), name='bank_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Launch the cron scheduler
start_scheduler()
