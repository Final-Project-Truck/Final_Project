import django.urls
from analytics.models import RequestCounter


class MyMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        instance = RequestCounter.objects.get_or_create(route=request.path)
        instance[0].counter += 1
        instance[0].save()
        return None
