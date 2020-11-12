from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# class PlayerCreationForm(UserCreationForm):
#     email = forms.EmailField(label='Email address', max_length=75)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('frontpage')

    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})
