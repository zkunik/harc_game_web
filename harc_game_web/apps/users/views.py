from django import forms
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.db import transaction
from django.forms import Select
from django.shortcuts import render, redirect, get_object_or_404, reverse

from apps.teams.models import Patrol
from apps.users.models import HarcgameUser, Scout


class HarcgameUserCreationForm(UserCreationForm):
    class Meta:
        model = HarcgameUser
        fields = ['email', 'nickname']


class ScoutCreationForm(forms.ModelForm):
    class Meta:
        model = Scout
        fields = ['initials', 'patrol', 'rank']

        labels = {
            "initials": "Inicjały",
            "patrol": "Zastęp",
            "rank": "Stopień harcerski"
        }
        widgets = {
            'rank': Select(attrs={'class': 'rpgui-list'}),
            'patrol': Select(attrs={'class': 'rpgui-list'}),
        }


@transaction.atomic
def signup(request):
    if request.method == "POST":
        user_form = HarcgameUserCreationForm(request.POST)
        scout_form = ScoutCreationForm(request.POST)

        if user_form.is_valid() and scout_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.scout.initials = scout_form.cleaned_data.get('initials')
            user.scout.patrol = scout_form.cleaned_data.get('patrol')
            user.scout.team = user.scout.patrol.team
            user.scout.rank = scout_form.cleaned_data.get('rank')
            user.save()
            login(request, user)
            return redirect('frontpage')

    else:
        user_form = HarcgameUserCreationForm()
        scout_form = ScoutCreationForm()

    return render(request, 'users/common.html', {
        'forms': [user_form, scout_form],
        'info': "Załóż konto"
    })


def view_profile(request, user_id):
    user = request.user if user_id is None else get_object_or_404(HarcgameUser, id=user_id)
    return render(request, 'users/view_profile.html', {
        'user': user,
        'allow_edit': bool(user == request.user)
    })


class HarcgameUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = HarcgameUser
        fields = ['nickname']


class ScoutChangeForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ScoutChangeForm, self).__init__(*args, **kwargs)
        self.fields['patrol'].queryset = Patrol.objects.filter(team=request.user.scout.team)

    class Meta:
        model = Scout
        fields = ['patrol', 'rank']

        labels = {
            "patrol": "Zastęp",
            "rank": "Stopień harcerski"
        }
        widgets = {
            'rank': Select(attrs={'class': 'rpgui-list'}),
            'patrol': Select(attrs={'class': 'rpgui-list'}),
        }


@login_required
@transaction.atomic
def edit_profile(request, user_id):
    user = get_object_or_404(HarcgameUser, id=user_id)
    if request.user != user:
        return redirect(reverse('view_profile', kwargs={"user_id": user_id}))

    if request.method == "POST":
        user_form = HarcgameUserChangeForm(request.POST, instance=user)
        scout_form = ScoutChangeForm(request, request.POST, instance=user.scout)

        if user_form.is_valid() and scout_form.is_valid():
            user = user_form.save()
            user.scout.patrol = scout_form.cleaned_data.get('patrol')
            user.scout.rank = scout_form.cleaned_data.get('rank')
            user.save()
            return redirect(reverse('view_profile', kwargs={"user_id": user_id}))

    else:
        user_form = HarcgameUserChangeForm(instance=user)
        scout_form = ScoutChangeForm(request=request, instance=user.scout)

    return render(request, 'users/common.html', {
        'forms': [user_form, scout_form],
        'info': "Edytuj profil"
    })


@login_required
@transaction.atomic
def change_password(request, user_id):
    user = get_object_or_404(HarcgameUser, id=user_id)
    if request.user != user:
        return redirect(reverse('view_profile', kwargs={"user_id": user_id}))

    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('view_profile', kwargs={"user_id": user_id}))

    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'users/common.html', {
        'forms': [password_form],
        'info': "Zmień hasło"
    })
