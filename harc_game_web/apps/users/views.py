from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from apps.users.models import HarcgameUser, Scout


class HarcgameUserCreationForm(UserCreationForm):
    class Meta:
        model = HarcgameUser
        fields = ['email', 'nickname']


class ScoutCreationForm(forms.ModelForm):
    class Meta:
        model = Scout
        fields = ['initials', 'patrol', 'team', 'rank']


def signup(request):
    if request.method == "POST":
        user_form = HarcgameUserCreationForm(request.POST)
        scout_form = ScoutCreationForm(request.POST)

        if user_form.is_valid() and scout_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.scout.initials = scout_form.cleaned_data.get('initials')
            user.scout.patrol = scout_form.cleaned_data.get('patrol')
            user.scout.team = scout_form.cleaned_data.get('team')
            user.scout.rank = scout_form.cleaned_data.get('rank')
            user.save()
            login(request, user)
            return redirect('frontpage')

    else:
        user_form = HarcgameUserCreationForm()
        scout_form = ScoutCreationForm()

    return render(request, 'users/signup.html', {'user_form': user_form, 'scout_form': scout_form})
