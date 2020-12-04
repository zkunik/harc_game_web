from collections import defaultdict

from django.shortcuts import render
from django.db.models import Sum

from apps.bank.models import Bank
from apps.core.utils import round_half_up, default_to_regular
from apps.teams.models import Team, Patrol
from apps.users.models import Scout


def calculate_user_score(user):
    """
    Function to calculate score of given user
    """
    score = Bank.objects.filter(accrual_deleted=False).filter(user=user).aggregate(Sum('accrual'))['accrual__sum']
    return score if score is not None else 0


def calculate_team_or_patrol_score(patrol_or_team):
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
    team_score = calculate_team_or_patrol_score(team)
    patrols_scores = [(patrol, calculate_team_or_patrol_score(patrol)) for patrol in Patrol.objects.filter(team=team)]
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


def view_team_details(request, team_id):
    """
    Function to view detailed info on scores
    """
    team = Team.objects.get(id=team_id)
    team_score = calculate_team_or_patrol_score(team)
    scouts = Scout.objects.filter(team=team)
    team_leader = scouts.filter(is_team_leader=True).first()

    weeks = [v["year_week"] for v in Bank.objects.values('year_week').distinct()]

    # week - user - netto/tax
    scout_accruals = defaultdict(lambda: defaultdict(int))
    taxes = {}

    accurals = Bank.objects.filter(accrual_deleted=False, user__scout__in=scouts)
    for week in weeks:
        taxes[week] = 0
        scores = accurals.filter(year_week=week).values('user', 'accrual_type').order_by().annotate(Sum('accrual'))
        for score in scores:
            accrual_type = score['accrual_type']
            scout = Scout.objects.get(user__id=score['user'])
            if accrual_type == "brutto":
                tax = int(round_half_up(score['accrual__sum'] * team.tax))
                taxes[week] += tax
                scout_accruals[week][scout] += score['accrual__sum'] - tax
            elif accrual_type == "tax":
                taxes[week] += score['accrual__sum']
            else:  # netto
                scout_accruals[week][scout] += score['accrual__sum']

    scout_accruals = default_to_regular(scout_accruals)

    return render(request, 'teams/view_details.html', {
        'team': team,
        'team_score': team_score,
        'leader': team_leader,
        'scout_accruals': scout_accruals,
        'taxes': taxes
    })

