from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
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
        return f"{self.email} ({self.nickname})"


class Scout(models.Model):
    """
    Harcerz (jako dodatkowe atrybuty użytkownika)
    """
    RANK_CHOICES = [
        ('', 'bez stopnia'),
        ('mł.', 'mł.'),
        ('wyw.', 'wyw.'),
        ('ćwik', 'ćwik'),
        ('HO', 'HO'),
        ('pwd. HO', 'pwd. HO'),
        ('HR', 'HR'),
        ('pwd. HR', 'pwd. HR'),
        ('phm. HR', 'phm. HR'),
        ('hm. HR', 'hm. HR'),
    ]
    user = models.OneToOneField(HarcgameUser, on_delete=models.CASCADE)
    initials = models.CharField(max_length=3)
    patrol = models.ForeignKey(Patrol, on_delete=models.RESTRICT, null=True, default=None, related_name='scouts')
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, null=True, default=None, related_name='scouts')
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='bezstopnia')
    is_patrol_leader = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['initials', 'patrol', 'team', 'rank']

    def __str__(self):
        return f"{self.rank} {self.user.nickname}"

    def get_minecraft_name(self):
        return "_".join(self.rank.replace(".", "").split(" ") + [self.user.nickname])


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

