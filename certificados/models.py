# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Certificado(models.Model):
    participante = models.CharField(max_length=400)
    carga = models.IntegerField()
    tipo = models.CharField(max_length=50, choices=(('PC', 'Participante'), ('OG', 'Organizador'), ('AU', 'Autor'), ('PR', 'Premio'),
                                                    ('POG', 'Professor Organizador'), ('PA', 'Palestrante')), default='PC')
    trabalho = models.CharField(max_length=300)
