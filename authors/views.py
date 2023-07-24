from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout, login, authenticate # para realizar a autenticação, login e logout do usuario
from django.contrib.auth.decorators import login_required # somente usuarios logados possa acessar a view


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



def login_view(request): #view para realizazr o login
    form = LoginForm()

    if request.POST:

        form = LoginForm(request.POST)
        login_url = reverse('authors:login')

        if form.is_valid():
            # authenticated_user = authenticate(
            #     username=form.cleaned_data.get('username', ''),
            #     password=form.cleaned_data.get('password', ''),
            # )

            username = request.POST["username"]
            password = request.POST["password"]
            authenticated_user = authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                messages.success(request, 'Your are logged in.')
                login(request, authenticated_user)
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid username or password')

        return redirect(login_url)

    
    return render(request, 'authors/pages/login.html', {
        'form': form,
    })


@login_required(login_url='authors:login')
def logout_view(request): #view para realizazr o logout
    logout(request)
    return redirect('authors:login')
