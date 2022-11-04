from django.contrib import admin
from django.urls import path,include, re_path
from . import views
urlpatterns = [
    path('hello',views.hello_world),
    path('task',views.task),
    path('',views.home_page),
    path('analytics', views.analytics),
    path('graphs', views.graphs),
    path('url/<slug:customname>',views.redirect_url),
    path('link-analytics/<slug:customname>',views.link_analytics),
    # Regex
    re_path(r'/*/',views.error_url),
]
