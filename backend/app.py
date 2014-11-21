from django.conf.urls import patterns, url

from oscar.core.application import Application
from oscar.apps.backend import views


class BackendApplication(Application):
    name = 'backend'

    backend_redirect_view = views.BackendRedirectView

    def get_urls(self):
        urls = [
            url(r'^$', self.backend_redirect_view.as_view(),
                name='backend-redirect'),
        ]
        return self.post_process_urls(patterns('', *urls))


application = BackendApplication()
