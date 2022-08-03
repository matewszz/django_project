from distutils.command.upload import upload
from unicodedata import category

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    # max_length determinar o max de caracter, tipo um varchar Sql #
    title = models.CharField(max_length=65)
    # models.CharField serve para criar interações que o usuario digite algo, tipo um blog #
    description = models.CharField(max_length=165)
    # O slug serve para realizar uma busca de algo, por exemplo um int que realiza um busca e retorna algo #
    slug = models.SlugField()
    # Para o usuário digitar um número inteiro #
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    serving = models.IntegerField()
    preparation_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    # DateTimeField realiza a documentação da data quando houver criado algo #
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # Serve para realizar o upload de uma imagem e o "upload_to='' é para informa para onde vai ser encaminhado a imagem quando o cliente upar + ano/mês/dia" #
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d')
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title
