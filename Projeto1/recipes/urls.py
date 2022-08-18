from django.urls import path
from recipes.views import contato, home, sobre

path ('', home),
path ('contato/', contato),
path ('sobre/', sobre),

