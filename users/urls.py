"""Defines URL patterns for users"""
from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
  # Registration page
  url(r'^register/$',
      views.register,
      name='register'),

  # Logout page
  url(r'^logout/$',
      views.logout_view,
      name='logout'),

  # Login page
  url(r'^login/$',
      login,
      {'template_name': 'users/login.html'},
      name='login'),
]
