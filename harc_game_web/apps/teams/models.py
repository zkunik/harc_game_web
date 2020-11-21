from django.db import models


class Team(models.Model):
    """
    Drużyna
    """
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    colors = models.CharField(max_length=100)
    tax = models.FloatField()

    @property
    def score(self):
        """
        Calculate teams score
        """
        score = 0
        for scout in self.scouts.all():
            score += scout.score
        return score

    def __str__(self):
        return self.name


class Patrol(models.Model):
    """
    Zastęp
    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True, default=None)

    @property
    def score(self):
        """
        Calculate teams score
        """
        score = 0
        for scout in self.scouts.all():
            score += scout.score
        return score

    def __str__(self):
        return self.name
