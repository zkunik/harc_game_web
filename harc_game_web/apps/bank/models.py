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
    accrual_extra_prize = models.CharField(max_length=200, default=None, null=True, blank=True)
    # accruals are marked as deleted, bit not deleted
    accrual_deleted = models.BooleanField(default=False)
    # Allowed types of accrual (it is mainly for ledger debugging):
    # "tax" - tax taken from team member
    # "netto" - ramaining prize afer tax, used for members
    # "brutto" - whole prize, not taxed, used for team leaders
    accrual_type = models.CharField(max_length=10)
    # Additional property, which needs to be calculated here, otherwise can't be used queries
    # It will be used to display prizes grouped by weeks of year
    # Format 2020-W46
    year_week = models.CharField(max_length=8)

    REQUIRED_FIELDS = ['user', 'date_accrued', 'documented_task', 'accrual', 'accrual_type']

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
        return f"{'DELETED' if self.accrual_deleted else ''} {self.date_accrued.date()} - {self.user.nickname} - {self.task} {self.accrual} pkt + {self.accrual_extra_prize}"
