from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [

    path('', views.home, name="home"),
    path('recipes/search/', views.search, name="recipe"),

    path('recipes/category/<int:category_id>/',
         views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('recipes/register_recipe/', views.register_recipe, name="register_recipe"),
    path('new_recipe/', views.new_recipe, name="new_recipe"),


]