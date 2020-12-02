from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone

from apps.shop.models import Request, Vote, CATEGORY_CHOICES, ItemOffer

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

    return render(request, 'shop/view_shop.html', {'offers_grouped': offers_grouped})


# Requests

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'content', 'link1', 'link2', 'link3', 'price', 'date']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        #self.fields['content'].widget.attrs['cols'] = 10
        self.fields['content'].widget.attrs.update({'style':'height:50%'})


def list_active_requests(request):
    """
    Function to list all requests
    """
    requests = Request.objects.exclude(is_active=False).order_by(
        F('date').desc(nulls_last=True)
    )
    return render(request, 'shop/list_active_requests.html', {'requests': requests})


def view_request(request, id):
    """
    Function to list a single request
    """
    req = Request.objects.get(id=id)
    return render(request, 'shop/view_request.html', {'request': req})


@login_required
def new_request(request):
    """
    Function create a request
    """

    # If request is POST, create a bound form (form with data)
    if request.method == "POST":
        form = RequestForm(request.POST)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the add request form

        # If form is invalid show form with errors again
        if form.is_valid():
            #  save data
            req = form.save()
            req.user = request.user
            req.save()
            return redirect('view_request', id=req.id)
    # if request is GET the show unbound form to the user
    else:
        form = RequestForm()
    return render(request, 'shop/edit_request.html', {'form': form})


@login_required
def edit_request(request, id):
    """
    Function edit a request
    """
    req = get_object_or_404(Request, id=id)
    if (not req.is_active) or (req.user.id is not request.user.id):
        return redirect(reverse('view_request', args=[req.id]))

    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=req)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update request form

        # If form is invalid show form with errors again
        if form.is_valid():
            form.save()
            return redirect(reverse('view_request', args=[req.id]))

    # if request is GET the show unbound form to the user, along with data
    else:
        form = RequestForm(instance=req)

    return render(request, 'shop/edit_request.html', {'form': form, 'request': req})


@login_required
def delete_request(request, id):
    """
    Function to delete a request
    """
    req = get_object_or_404(Request, id=id)
    if req.user.id is request.user.id:
        req.delete()

    return redirect(reverse('active_requests'))
