from django.urls import path

from . import views

app_name: str = 'pages'

urlpatterns = [
    path('about/', views.AboutDetailView.as_view(), name='about'),
    path('rules/', views.RulesDetailView.as_view(), name='rules'),
]
