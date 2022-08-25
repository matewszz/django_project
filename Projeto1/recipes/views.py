from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html',
                  context={
                      'name': 'matos'
                  })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html',
                  context={
                      'is_detail_page': True,
                  })
