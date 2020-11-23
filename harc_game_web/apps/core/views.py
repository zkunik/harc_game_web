from django.shortcuts import render

# Temporal patch to have posts on home page
from apps.posts.views import list_active_posts

def frontpage(request):
    return list_active_posts(request)
#    return render(request, 'core/frontpage.html')
