from django.views import generic
from utils import login_in_backend


class BackendRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return login_in_backend(self.request.user)
