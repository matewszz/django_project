# Esse arquivo vai ser utilizado pelo python para carregar tudo que for preciso 
# inicialmente quando for importado o forms.py
# Facilitando o uso de multiplos forms dentro de um mesmo app
# todo form criado deve ser importado no __init__.py

# flake8: noqa # -- comando para o flake8 não fazer analise desse arquivo.

from .RegisterRecipe import RegisterRecipeForm
