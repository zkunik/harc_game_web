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
        
        bank = Bank.objects.order_by(F('date_accrued').desc(nulls_last=True))
        prizes = []
        for b in bank.values('year_week','user').order_by().annotate(Sum('accrual')):
            prizes.append({
                'nickname': HarcgameUser.objects.get(pk=b['user']).nickname, 
                'accrual_for_a_week': b['accrual__sum'],
                'year_week': b['year_week']
            })
        weeks = [account['year_week'] for account in Bank.objects.values('year_week').distinct()]
        return render(request, 'bank/report.html', {'bank': bank, 'prizes': prizes, 'weeks': weeks})