from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from apps.users.managers import CustomUserManager


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


class Team(models.Model):
    """
    Drużyna
    """
    name = models.CharField(max_length=100)
    colors = models.CharField(max_length=100)
    tax = models.FloatField()

    def __str__(self):
        return self.name


class Patrol(models.Model):
    """
    Zastęp
    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True, default=None)

    def __str__(self):
        return self.name


class Scout(models.Model):
    """
    Harcerz (jako dodatkowe atrybuty użytkownika)
    """
    user = models.OneToOneField(HarcgameUser, on_delete=models.CASCADE)
    initials = models.CharField(max_length=3)
    patrol = models.ForeignKey(Patrol, on_delete=models.RESTRICT, null=True, default=None)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True, default=None)
    rank = models.CharField(max_length=20)
    is_patrol_leader = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['initials', 'patrol', 'team', 'rank']


@receiver(models.signals.post_save, sender=HarcgameUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Scout.objects.create(user=instance)
    instance.scout.save()

