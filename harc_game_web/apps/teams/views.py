from django.shortcuts import render
from django.views import View

from apps.teams.models import Team

class TeamView(View):

    def get(self, request, *args, **kwargs):
        """
        Function to list all teams
        """
        teams = Team.objects.all()
        return render(request, 'teams/list_teams.html', {'teams': teams})

    def view(request, id):
        """
        Function to view
        """
        team = Team.objects.get(id=id)
        return render(request, 'teams/view.html', {'team': team})

