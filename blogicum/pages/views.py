from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render


class AboutDetailView(TemplateView):
    template_name = 'pages/about.html'

class RulesDetailView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
