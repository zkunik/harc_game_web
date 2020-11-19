from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.utils import timezone

from apps.users.managers import CustomUserManager
from apps.teams.models import Team, Patrol


class HarcgameUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    nickname = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Scout(models.Model):
    """
    Harcerz (jako dodatkowe atrybuty użytkownika)
    """
    user = models.OneToOneField(HarcgameUser, on_delete=models.CASCADE)
    initials = models.CharField(max_length=3)
    patrol = models.ForeignKey(Patrol, on_delete=models.RESTRICT, null=True, default=None, related_name='scouts')
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True, default=None, related_name='scouts')
    rank = models.CharField(max_length=20)
    is_patrol_leader = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['initials', 'patrol', 'team', 'rank']

    @property
    def score(self):
        """
        Obliczenie wyniku
        """
        # import is here, otherwise we have a cyclic import
        from apps.tasks.models import Task, DocumentedTask, TaskApproval

        score = Task.objects.filter(documented_tasks__user=self.user).\
                             filter(documented_tasks__task_approval__is_accepted=True).\
                             aggregate(Sum('prize'))['prize__sum']

        return score if score != None else 0

    def __str__(self):
        return self.user.nickname


@receiver(models.signals.post_save, sender=HarcgameUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Scout.objects.create(user=instance)
    instance.scout.save()


class FreeDay(models.Model):
    """
    Dzień wolny osoby sprawdzającej zadania
    """
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    day = models.DateField(null=True, default=None)

