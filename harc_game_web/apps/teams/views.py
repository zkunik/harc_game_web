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
        scouts = Scout.objects.filter(team=team)
        team_leader = scouts.filter(is_team_leader=True).first()

# def score(self):
    #     """
    #     Obliczenie wyniku
    #     """
    #     from apps.tasks.models import Task, DocumentedTask, TaskApproval

    #     print(DocumentedTask.objects.all())
    #     print(DocumentedTask.objects.select_related('task')) 

    #     #return Task.objects.filter(user=self.user).select_related('DocumentedTask').aggregate(Sum('prize'))

    #     print(
    #         #DocumentedTask.objects.filter(user=self.user).filter(taskapproval__is_accepted=True)
    #         TaskApproval.objects.all()#filter(is_accepted=True).all()
    #     )
    #     return Task.objects.aggregate(Sum('prize'))
    
        print(TaskApproval.objects.all())

        return render(request, 'teams/view.html', {'team': team, 'leader': team_leader, 'patrols': patrols, 'scouts': scouts})

