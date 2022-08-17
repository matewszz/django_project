from django.contrib import admin
from django.http import response
from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.home),
    path('recipes/category/<int:category_id>/',views.category, name="category"),
    path('recipes/<int:id>/', views.Recipe),
]
