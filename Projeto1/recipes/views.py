from django.db.models import Q
from django.http import Http404, HttpResponse #F401
from django.shortcuts import get_list_or_404, get_object_or_404, render
from recipes.models import Recipe
from django.core.paginator import Paginator


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')
    usuario_paginator = Paginator(recipes, 3)   # Variavel dos obj e a quantidade dessa variavel
    page_num = request.GET.get('page')          # verifica quais posts deve mostrar na página determinada
    page = usuario_paginator.get_page(page_num) # Django está se situando em qual página da paginação ele está
    
    return render(request, 'recipes/pages/home.html', {'page': page})


def category(request, category_id):
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


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
 
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # O 'Q' serve para o django para realizar a busca por um nome, buscar algo nessa variaveis, nessa caso a busca vai ser feita em palavras que estajam no titulo ou na descrição.
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes,
    })
