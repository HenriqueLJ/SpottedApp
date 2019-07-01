from django.db import models
from django.db.models import CharField, Model

# Create your models here.

class Spotteds(models.Model):
    titulo = models.CharField(max_length=64)
    texto = models.TextField(max_length=768)
    categoria = models.CharField(max_length=16)
    aceito = models.BooleanField(default=False)
    avaliado = models.BooleanField(default=False)
