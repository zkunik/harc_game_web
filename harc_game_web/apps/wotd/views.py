from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

import datetime

from apps.wotd.models import WordOfTheDay


class WordOfTheDayView(View):

    def __verify(self, word, guess):
        """
        slugify will take care about spaces, special characters, polish characters, capital letters, etc
        looks like a good/quick solution for clan text comparing

        https://docs.djangoproject.com/en/3.1/ref/utils/#django.utils.text.slugify
        - Converting to ASCII if allow_unicode is False (the default).
        - Converting to lowercase.
        - Removing characters that aren’t alphanumerics, underscores, hyphens, or whitespace.
        - Removing leading and trailing whitespace.
        - Replacing any whitespace or repeated dashes with single dashes.
        """
        try:
            return slugify(word.answer) == slugify(guess)
        except AttributeError:
            return False

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
        try:
            # we will not use get but filter, otherwise if by mistake there are two words a day, we will get MultipleObjectsReturned
            word_of_the_day = WordOfTheDay.objects.filter(date = timezone.now()).first()
        except ObjectDoesNotExist:
            word_of_the_day = WordOfTheDay()
        try:
            word_for_tomorrow = WordOfTheDay.objects.filter(date = timezone.now() + datetime.timedelta(days=1)).first()
        except ObjectDoesNotExist:
            word_for_tomorrow= WordOfTheDay()
        today_guess = request.GET.get('today_guess', '')
        tomorrow_guess = request.GET.get('tomorrow_guess', '')

        return render(request, 'wotd/view.html', {
            'words_of_the_past': words_of_the_past,
            'word_of_the_day': word_of_the_day,
            'word_for_tomorrow': word_for_tomorrow,
            'today_guess': today_guess,
            'today_guess_is_correct': self.__verify(word_of_the_day, today_guess),
            'tomorrow_guess': tomorrow_guess,
            'tomorrow_guess_is_correct': self.__verify(word_for_tomorrow, tomorrow_guess)
        })
