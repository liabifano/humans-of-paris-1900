from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('facemap', views.cluster, name='facemap'),
    path('yourdoppelganger', views.yourdoppelganger, name='yourdoppelganger'),
    path('person/<str:name>/', views.person, name='person'),
    path('tag/<str:tag>/', views.tag, name='tag')
]