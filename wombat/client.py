# -*- coding: utf-8 -*-
import simplejson
import requests
from django.conf import settings

from django.db.models import get_model
from serializer import serialize

def push(app_name,model_name):
    res = []
    object_list = get_model(app_name,model_name).objects.all()
    data = [serialize(item) for item in object_list]
    payload = simplejson.dumps({'usdas': data})
    headers = {
        'Content-Type': 'application/json',
        'X-Hub-Store': settings.WOMBAT_STORE,
        'X-Hub-Access-Token': settings.WOMBAT_TOKEN
    }
    r = requests.post(settings.WOMBAT_URL, data=payload, headers=headers)
    res.append(r.status_code)
    return res