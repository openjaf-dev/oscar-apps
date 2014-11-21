# -*- coding: utf-8 -*-
'''
Created on 17/11/2014

@author: José Andrés Hernández Bustio
'''

from django.core.management.base import BaseCommand
from apps.wombat.client import push

class Command(BaseCommand):
    args = '<argumento1 argumento2 ...>'
    help = 'Enviar objetos para wombat'

    def handle(self, *args, **options):
        push(args[0],args[1])
        print 'Se ejecuto el comando con exito'

