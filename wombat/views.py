'''
Created on 16/11/2014

@author: José Andrés Hernández Bustio 
'''

from django.views import generic


class BackendRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return login_in_backend(self.request.user)
