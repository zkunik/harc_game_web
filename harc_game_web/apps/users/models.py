from django.db import models

class Team(models.Model):
    """
    Drużyna
    """
    name = models.CharField(max_length=100)
    colors = models.CharField(max_length=100)
    tax = models.FloatField()


class Patrol(models.Model):
    """
    Zastęp
    """
    name = models.CharField(max_length=100)


class Scout(models.Model):
    """
    Id gracza (generowane automatycznie)
    Inicjały
    Ksywa
    Stopień
    Dodatkowa funkcja
    Drużyna
    Zastęp
    """
    inintials = models.CharField(max_length=3)
    nickname = models.CharField(max_length=20)
    rank = models.CharField(max_length=20)
    is_patrol_leader = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)
    patrol = models.ForeignKey(Patrol, on_delete=models.RESTRICT)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
