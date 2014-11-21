# -*- coding: utf-8 -*-
'''
Created on 15/10/2014

@author: José Andrés Hernández Bustio
'''

def serialize(item):
    vals = {}
    for field in item._meta.concrete_fields:
        try:
            if getattr(item, field.name)==None:
                value=""
            else:
                value = str(getattr(item, field.name))
        except:
            value = ""
        vals[field.name] = value
    
    return vals