from django.urls import path

from recipes import views

urlpatterns = [

    path('', views.home),
    path('recipe/<int:id>', views.recipe),

]
