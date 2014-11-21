# -*- coding: utf-8 -*-
'''
Created on 16/11/2014

@author: José Andrés Hernández Bustio 
'''

from django.db import models

class WombatClient(models.Model):
    url = models.CharField(max_length=200)
    store = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
