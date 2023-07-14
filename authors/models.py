from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)

    def __str__(self):
        return self.nome
