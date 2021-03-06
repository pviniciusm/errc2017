# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participante', models.CharField(max_length=400)),
                ('carga', models.IntegerField()),
                ('tipo', models.CharField(choices=[('PC', 'Participante'), ('OG', 'Organizador'), ('AU', 'Autor'), ('POG', 'Professor Organizador'), ('PA', 'Palestrante')], default='PC', max_length=50)),
                ('trabalho', models.CharField(max_length=300)),
            ],
        ),
    ]
