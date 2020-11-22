from django.shortcuts import render
from django.views import View
from django.db.models import F, Sum

from apps.bank.models import Bank
from apps.users.models import HarcgameUser


class BankReport(View):

    def get(self, request, *args, **kwargs):
        """
        Function to list all accrurals in bank
        """
        # All accruals in bank, which are not marked for delete
        accruals = Bank.objects.filter(accrual_deleted=False).order_by(F('date_accrued').desc(nulls_last=True))
        # Sum up the prizes of each week
        prizes = []
        for account in accruals.values('year_week','user').order_by().annotate(Sum('accrual')):
            prizes.append({
                'nickname': HarcgameUser.objects.get(pk=account['user']).nickname,
                'accrual_for_a_week': account['accrual__sum'],
                'year_week': account['year_week']
            })
        # Distinct list of the weeks
        weeks = [account['year_week'] for account in Bank.objects.filter(accrual_deleted=False).values('year_week').distinct()]
        return render(request, 'bank/report.html', {'bank': accruals, 'prizes': prizes, 'weeks': weeks})