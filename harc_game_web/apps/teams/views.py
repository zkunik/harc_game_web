from django.shortcuts import render
from django.views import View

from apps.teams.models import Team, Patrol
from apps.users.models import Scout
from apps.tasks.models import Task, DocumentedTask, TaskApproval


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
        patrols = Patrol.objects.filter(team=team)
        scouts = Scout.objects.filter(team=team).annotate()
        team_leader = scouts.filter(is_team_leader=True).first()

        return render(request, 'teams/view.html', {'team': team, 'leader': team_leader, 'patrols': patrols, 'scouts': scouts})

