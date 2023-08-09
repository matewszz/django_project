from django.contrib import admin
from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_at', 'is_published', 'author', # São os itens desejados para aparecer no admin
    list_display_links = 'title', 'id', # links nos itens selecionados
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps', # cria um campo de busca e nele busca os campos passados
    list_filter = 'category', 'author', 'is_published', # cria filtros com os campos passados
    list_per_page = 10 # o número de itens que vai aparecer
    list_editable = 'is_published', # para adicionar a opção de alterar um dado booleano
    ordering = '-id', # para ordenar os dados
    prepopulated_fields = {"slug": ["title"]} # o campo slug vai receber o que tiver no title já formatado
