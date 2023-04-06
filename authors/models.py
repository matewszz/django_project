from django.db import models

# Create your models here.

from django.db import models


SEXO_CHOICES = (
    ('a', 'ATV'),
    ('r', 'RTV')
)


class User(models.Model):
    nome = models.CharField(max_length=30)
    data_nascimento = models.DateField(blank=True, null=True) # esse campo não é obrigatorio
    acesso = models.CharField(max_length=3, choices=SEXO_CHOICES)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.nome