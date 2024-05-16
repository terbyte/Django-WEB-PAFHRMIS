# custom_middleware.py
from django.http import HttpResponseNotFound
from django.template import loader

class HandleBadRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            template = loader.get_template('other/404.html')
            return HttpResponseNotFound(template.render())
        return response
