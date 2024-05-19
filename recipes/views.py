import os
from django.db.models import Q  # Esse import serve para melhorar o search com uma busca por algum atributo do arquivo
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from recipes.models import Recipe
from django.core.paginator import Paginator
from recipes.forms import RegisterRecipeForm
from django.contrib.auth.decorators import login_required # somente usuarios logados possa acessar a view
from django.contrib import messages
from django.shortcuts import redirect, render
from random import randint

PER_PAGE = os.environ.get('PER_PAGE', 6) # Variavel de produção, quando alterado o valor no .env é realizado a alteração por aqui 
RANDOM = str(randint(0, 100))

def home(request):

    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    usuario_paginator = Paginator(recipes, PER_PAGE)
    page_num = request.GET.get('page')
    page_obj = usuario_paginator.get_page(page_num)

    context = {}
    context['page'] = page_obj
    context['recipes'] = recipes

    return render(request, 'recipes/pages/home.html', context=context) # {'page': page}


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
    form = RegisterRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    context = {'form': form}

    
    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
            
        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect('authors:dashboard')
    
    else:
        return render(request, 'recipes/pages/new_recipe.html', context)
