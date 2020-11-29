from django.shortcuts import render
from django.db.models import Sum

from apps.teams.models import Team, Patrol
from apps.users.models import Scout
from apps.bank.models import Bank


def calculate_user_score(user):
    """
    Function to calculate score of given user
    """
    score = Bank.objects.filter(accrual_deleted=False).filter(user=user).aggregate(Sum('accrual'))['accrual__sum']
    return score if score is not None else 0


def calculate_team_patrol_score(patrol_or_team):
    """
    Function to calculate score of team of patrol (depending on what was passed as arg)
    """
    return sum([calculate_user_score(scout.user) for scout in patrol_or_team.scouts.all()])


def view_teams_list(request, *args, **kwargs):
    """
    Function to list all teams
    """
    teams = Team.objects.all()
    return render(request, 'teams/list_teams.html', {'teams': teams})


def view_team(request, team_id):
    """
    Function to view
    """
    team = Team.objects.get(id=team_id)
    team_score = calculate_team_patrol_score(team)
    patrols_scores = [(patrol, calculate_team_patrol_score(patrol)) for patrol in Patrol.objects.filter(team=team)]
    scouts = Scout.objects.filter(team=team).annotate()
    scouts_scores = [(scout, calculate_user_score(scout.user)) for scout in scouts]
    team_leader = scouts.filter(is_team_leader=True).first()

    return render(request, 'teams/view.html', {
        'team': team,
        'team_score': team_score,
        'leader': team_leader,
        'patrols_scores': patrols_scores,
        'scouts_scores': scouts_scores
    })
