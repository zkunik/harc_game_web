from django.contrib import admin

from apps.teams.models import Team, Patrol

admin.site.register(Team)
admin.site.register(Patrol)