from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.username = form.cleaned_data.get("email")
            user.save()
            messages.success(request, 'Your user is created, please log in.')
            
            return redirect('authors:login')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'authors/pages/register_view.html', context=context)


def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login_view.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    return render(request, 'authors/pages/login_view.html', )
