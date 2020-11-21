from datetime import timedelta

from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError

from apps.users.models import HarcgameUser
from apps.tasks.models import Task, DocumentedTask, TaskApproval
from apps.users.models import Scout


class Bank(models.Model):
    """
    Model bank zaakceptowanych taskow

    Bank
        Historia przyznawania punktów (brutto, przed podatkiem)
        Atrybuty:
            Data (dzień i godzina)
            Id gracza
            zaliczone zadanie (z zadania można wziąć nagrodę)

    """
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    date_accrued = models.DateTimeField(default=timezone.now)
    documented_task = models.ForeignKey(DocumentedTask, on_delete=models.RESTRICT, null=True, default=None)
    accrual = models.IntegerField(default=0, null=True)
    accrual_extra_prize = models.CharField(max_length=200, default=None, null=True)
    # Allowed types of accrual (it is mainly for ledger debugging):
    # "tax" - tax taken from team member
    # "netto" - ramaining prize afer tax, used for members
    # "brutto" - whole prize, not taxed, used for team leaders
    accrual_type = models.CharField(max_length=10)
    # Additional property, which needs to be calculated here, otherwise can't be used queries
    # It will be used to display prizes grouped by weeks of year
    # Format 2020-W46
    year_week = models.CharField(max_length=8)

    REQUIRED_FIELDS = ['user', 'date_accrued', 'documented_task', 'accrual', "accrual_type"]
    
    @property
    def task(self):
        return self.documented_task.task
    
    def save(self, *args, **kwargs):
        # Calculate the year and week number
        # As we treat the week as Saturday through Friday, we need to move it by 2 days
        # As normally, the week is Monday through Sunday
        self.year_week = (self.date_accrued + timedelta(days=2)).strftime('%Y-W%W')
        return super(Bank, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date_accrued.date()} - {self.user.nickname} - {self.task} {self.accrual} pkt + {self.accrual_extra_prize}"


@receiver(models.signals.post_save, sender=TaskApproval)
def accure_task_signal(sender, instance, created, **kwargs):
    # If task is accepted, we can accure it
    if instance.is_accepted:
        # But first, let's verify if it was not accured yet
        if Bank.objects.filter(user=instance.documented_task.user, documented_task=instance.documented_task).count() == 0:
            # If this is team leader, just assign the prize to him
            if instance.documented_task.user.scout.is_team_leader:
                Bank.objects.create(
                    user=instance.documented_task.user, 
                    documented_task=instance.documented_task,
                    accrual=instance.documented_task.task.prize,
                    accrual_extra_prize=instance.documented_task.task.extra_prize,
                    accrual_type='brutto'
                )
            else:
                # Add price for the team member and deduct tax
                Bank.objects.create(
                    user=instance.documented_task.user, 
                    documented_task=instance.documented_task,
                    accrual=instance.documented_task.task.prize * (1-instance.documented_task.user.scout.team.tax),
                    accrual_extra_prize=instance.documented_task.task.extra_prize,
                    accrual_type='netto'
                )
                # And the tax for the team leader
                try:
                    try:
                        Bank.objects.create(
                            user=Scout.objects.get(team=instance.documented_task.user.scout.team, is_team_leader=True).user, 
                            documented_task=instance.documented_task,
                            accrual=instance.documented_task.task.prize * instance.documented_task.user.scout.team.tax,
                            accrual_extra_prize=None,
                            accrual_type='tax'
                        )
                    except MultipleObjectsReturned:
                        ValueError(f"{instance.documented_task.user.scout.team} ma więcej niż jednego drużynowego!")                    
                except ObjectDoesNotExist:
                    raise ValueError(f"{instance.documented_task.user} nie jest w żadnej drużynie!")
