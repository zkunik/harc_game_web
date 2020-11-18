from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.db.models import F

import datetime

from apps.wotd.models import WordOfTheDay

class WordOfTheDayView(View):

    def _verify(self, word, guess):
        return (word.answer == guess)

    def get(self, request, *args, **kwargs):
        """
        Hasła dnia
            Dzisiejsze hasło dnia
            Jutrzejsze hasło dnia
            Formularz do sprawdzania poprawności hasła dnia
            Poprzednie hasła dnia z odpowiedziami

        """

        # Firltrowanie pro datach
        words_of_the_past = WordOfTheDay.objects.all().exclude(date__gte = timezone.now()).order_by(F('date').desc(nulls_last=True))
        word_of_the_day = WordOfTheDay.objects.filter(date = timezone.now())[0]
        word_for_tomorrow = WordOfTheDay.objects.filter(date = timezone.now() + datetime.timedelta(days=1))[0]
        today_guess = request.GET.get('today_guess', '')
        tomorrow_guess = request.GET.get('tomorrow_guess', '')

        return render(request, 'wotd/view.html', {
            'words_of_the_past': words_of_the_past,
            'word_of_the_day': word_of_the_day,
            'word_for_tomorrow': word_for_tomorrow,
            'today_guess': today_guess,
            'today_guess_is_correct': self._verify(word_of_the_day, today_guess),
            'tomorrow_guess': tomorrow_guess,
            'tomorrow_guess_is_correct': self._verify(word_for_tomorrow, tomorrow_guess)
        })
