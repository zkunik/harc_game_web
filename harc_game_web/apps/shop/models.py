from django.db import models
from django.utils import timezone

from apps.users.models import HarcgameUser


"""
Harcerze powinni widzieć, co będą mogli kupić w grze za punkty zdobyte za zadania w aplikacji. Należy stworzyć podstronę (app) zawierającą aktualną ofertę.
Harcerz może również zgłosić prośbę o jakiś przedmiot poprzez formularz próśb.

Zmiany w bazie danych:

tabela z przedmiotami z Minecrafta (zewnętrzny link do ikony, nazwa angielska, nazwa polska - wszystkie dane na bazie https://minecraft.gamepedia.com/Minecraft_Wiki )
tabela z innymi rzeczami do kupienia (obrazek, nazwa, opis) (może być połączona z tabelą wyżej + dodanie "category" ?)
tabela oferty sklepu (id przedmiotu, cena, dzień)
tabela z logiem próśb (user id, prośba, proponowana cena, data) głosowanie?
Zmiany w navbarze:

"""

class Request(models.Model):
    """
    Model prośby

    tabela z logiem próśb
    Atrybuty:
        user id (user)
        prośba (content)
        proponowana cena (price)
        data (date)

    (głosowanie?)
    """

    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    content = models.TextField('Opis zapotrzebowania', help_text='Można używać tagów HTML')
    link1 = models.CharField('Link 1', max_length=400, null=True, default="", blank=True)
    link2 = models.CharField('Link 2', max_length=400, null=True, default="", blank=True)
    link3 = models.CharField('Link 3', max_length=400, null=True, default="", blank=True)
    price = models.IntegerField('Cena', default=0, null=True)
    date = models.DateField('Na kiedy jest to potrzebne', default=timezone.now)

    class Meta:
        verbose_name = "prośba"
        verbose_name_plural = "log próśb"

    def __str__(self):
        return f'{self.content[:30]} - created by {self.user}'


class Vote(models.Model):
    """
    Model głosu na prośbę
    """

    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    request = models.ForeignKey(Request, on_delete=models.RESTRICT, null=True, default=None)

    class Meta:
        verbose_name = "głos na prośbę"
        verbose_name_plural = "głosy na prośby"

    def __str__(self):
        return f"{self.user} - {self.request}"