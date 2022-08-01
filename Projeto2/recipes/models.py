from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=65)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=65) # max_length determinar o max de caracter, tipo um varchar Sql #
    description = models.CharField(max_length=165) # models.CharField serve para criar interações que o usuario digite algo, tipo um blog #
    slug = models.SlugField() #O slug serve para realizar uma busca de algo, por exemplo um int que realiza um busca e retorna algo #
    preparation_time = models.IntegerField() # Para o usuário digitar um número inteiro #
    preparation_time_unit = models.CharField(max_length=65)
    serving = models.IntegerField()
    preparation_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # DateTimeField realiza a documentação da data quando houver criado algo #
    update_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d') # Serve para realizar o upload de uma imagem e o "upload_to='' é para informa para onde vai ser encaminhado a imagem quando o cliente upar + ano/mês/dia" #
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
            User, on_delete=models.SET_NULL, null=True
    )
    
    def __str__(self):
        return self.title
