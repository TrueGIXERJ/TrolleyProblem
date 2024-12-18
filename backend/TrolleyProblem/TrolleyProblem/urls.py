"""
URL configuration for TrolleyProblem project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Bookings.urls')),
    path('accounts/', include('allauth.urls')),
]
