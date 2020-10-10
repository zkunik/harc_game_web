"""
harc_game_web URL Configuration
"""
from django.contrib import admin
from django.urls import path
from apps.core.views import frontpage, signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup')
]
