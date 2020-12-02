from django.shortcuts import render
from apps.shop.models import CATEGORY_CHOICES, ItemOffer
"""
Harcerze powinni widzieć, co będą mogli kupić w grze za punkty zdobyte za zadania w aplikacji. Należy stworzyć podstronę (app) zawierającą aktualną ofertę.
Harcerz może również zgłosić prośbę o jakiś przedmiot poprzez formularz próśb.

Podstrona oferty sklepu (mogą być 2 widoki albo 1 - do przemyślenia/sprawdzenia)

subnavbar
widoki:
-- tabela z aktualnymi ofertami
-- prosty formularz próśb z wyświetlaniem próśb poniżej
"""


def view_shop_offers(request):
    """
    Function to list all posts
    """
    offers_available = ItemOffer.objects.filter(is_available=True)
    offers_grouped = {}
    for category_search, category_name in CATEGORY_CHOICES:
        offers_grouped[category_name] = offers_available.filter(item__category=category_search)

    return render(request, 'shop/view.html', {'offers_grouped': offers_grouped})
