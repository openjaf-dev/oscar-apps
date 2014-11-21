# -*- coding: utf-8 -*-
'''
Created on 16/11/2014

@author: José Andrés Hernández Bustio 
'''

from django.contrib import admin
from django.db.models import get_model

WombatClient = get_model('wombat', 'WombatClient')

admin.site.register(WombatClient)
