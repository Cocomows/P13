from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Votre compte a bien été créé, {}! Vous pouvez vous connecter.'.format(username))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.warning(request, "Vous avez été déconnecté")
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'users/profile.html')

