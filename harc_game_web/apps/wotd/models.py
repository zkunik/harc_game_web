from django.db import models, IntegrityError
from django.utils.text import slugify
from django.utils import timezone

class WordOfTheDay(models.Model):
    """
    Odpowiedzi w formie daty lub słowa na pytanie danego dnia 

    Hasło dnia ma być podawane podczas wykonywania zadania danego dnia w celu uniknięcia oszustw

    Atrybuty:
        Id hasła (generowane automatycznie)
        Treść pytania (“zagadki”)
        Podpowiedź (link)
        Hasło dnia (rozwiązanie)
        Dzień, do którego przypisane jest hasło
        """
        
    #id jest tworzone automatycznie
    question = models.TextField(help_text='Można używać tagów HTML')
    hint = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    date = models.DateField('Kiedy ma być opublikowany', default=timezone.now)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            # Newly created object, so set timestamp
            self.date_time = timezone.now()
        return super(WordOfTheDay, self).save(*args, **kwargs)

    def __str__(self):
        return f'Pytanie na {self.date}'