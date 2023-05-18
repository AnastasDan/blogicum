from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutDetailView(TemplateView):
    template_name: str = 'pages/about.html'


class RulesDetailView(TemplateView):
    template_name: str = 'pages/rules.html'


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, 'pages/404.html', status=404)


def server_error(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    return render(request, 'pages/403csrf.html', status=403)
