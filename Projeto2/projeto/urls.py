from django.contrib import admin
from django.http import response
from django.urls import include, path
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("sobre/", include('recipes.urls')),

]
