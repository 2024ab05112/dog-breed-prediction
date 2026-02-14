from django.contrib import admin
from django.urls import path, include
from .proxy import proxy_view

urlpatterns = [
    path('', include('webapp.urls')),
    
    # We no longer proxy Grafana/Prometheus/API through Django.
    # They are accessible via their own LoadBalancer URLs.
]
