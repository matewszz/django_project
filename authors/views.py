from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.contrib.auth import logout, login, authenticate # para realizar a autenticação, login e logout do usuario
from django.contrib.auth.decorators import login_required # somente usuarios logados possa acessar a view
from recipes.models import Recipe

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

        return redirect('authors:dashboard')

    
    return render(request, 'authors/pages/login.html', {
        'form': form,
    })


@login_required(login_url='authors:login')
def logout_view(request): #view para realizazr o logout
    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )

    context = {
        'recipes': recipes,
    }

    return render(request,'authors/pages/dashboard.html', context)


@login_required(login_url='authors:login')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        is_published=False,
        author=request.user,
        id=id,
    )

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm( # esse tipo de form fica vinculado aos dados do model. então os dados aparecem para o user editar.
        data=request.POST or None,
        files=request.FILES or None, # deve sempre ter esse comando no form para indicar o tráfego de arquivos.
        instance=recipe,
    )

    context = {
        'recipes': recipe,
        'form': form,
    }

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))
    
    return render(request,'authors/pages/dashboard_recipe.html', context)

@login_required(login_url='authors:login')
def dashboard_recipe_delete(request, id):
    recipe = Recipe.objects.get(
        is_published=False,
        author=request.user,
        id=id,
    )

    if not recipe:
        raise Http404()
    
    recipe.delete()
    messages.success(request, 'Recipe deleted successfully!')
    return redirect('authors:dashboard')