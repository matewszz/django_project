from django.db.models import Q  # Esse import serve para melhorar o search com uma busca por algum atributo do arquivo
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from recipes.models import Recipe
from django.core.paginator import Paginator
from recipes.forms import RegisterRecipeForm
from django.contrib.auth.decorators import login_required # somente usuarios logados possa acessar a view
from django.contrib import messages
from django.shortcuts import redirect, render
from slug import slug
from random import randint

PER_PAGE = 9 # Variavel de produção, quando alterado o valor no .env é realizado a alteração por aqui 
RANDOM = str(randint(0, 100))

def home(request):

    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    usuario_paginator = Paginator(recipes, PER_PAGE)   # Variavel dos obj e a quantidade dessa variavel
    page_num = request.GET.get('page')          # verifica quais posts deve mostrar na página determinada
    page = usuario_paginator.get_page(page_num) # Django está se situando em qual página da paginação ele está

    return render(request, 'recipes/pages/home.html', {'page': page})


def category(request, category_id):
    try:
        recipes = get_list_or_404(
            Recipe.objects.filter(
                category__id=category_id,
                is_published=True,
            ).order_by('-id')
        )
        return render(request, 'recipes/pages/category.html', context={
            'recipes': recipes,
            'title': f'{recipes[0].category.name} - Category | '
        })
    except UnboundLocalError:
        return render(request, 'recipes/pages/404.html')


def recipe(request, id):
    try:
        recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
        return render(request, 'recipes/pages/recipe-view.html', context={
            'recipe': recipe,
            'is_detail_page': True,
        })
    except recipe.DoesNotExist:
        return render(request, 'recipes/pages/404.html')


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(

        # O 'Q' serve para o django para realizar a busca por um nome, buscar
        # algo nessa variaveis, nessa caso a busca vai ser feita em palavras
        # que estajam no titulo ou na descrição.
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes,
    })


@login_required(login_url='authors:login')
def register_recipe(request): 
    form = RegisterRecipeForm()

    return render(request, 'recipes/pages/new_recipe.html', {
        'form': form,
    })


@login_required(login_url='authors:login')
def new_recipe(request):
    form = RegisterRecipeForm( # esse tipo de form fica vinculado aos dados do model. então os dados aparecem para o user editar.
        data=request.POST or None,
        files=request.FILES or None, # deve sempre ter esse comando no form para indicar o tráfego de arquivos.
    )

    context = {'form': form}

    
    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        title_recipe = form.cleaned_data['title']
        recipe.slug = slug(title_recipe + RANDOM)
            
        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect('authors:dashboard')
    
    else:
        return render(request, 'recipes/pages/new_recipe.html', context)
