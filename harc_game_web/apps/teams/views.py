from django.shortcuts import render
from django import forms

from apps.users.models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'colors', 'tax']

    def list(request):
        """
        Function to list all posts
        """
        teams = Team.objects.all()
        print(teams)
        return render(request, 'teams/list_teams.html', {'teams': teams})

    def view(request, id):
        """
        Function to view
        """
        team = Team.objects.get(id=id)
        return render(request, 'teams/view.html', {'team': team})

