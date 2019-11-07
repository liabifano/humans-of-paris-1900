from django.urls import path
from . import views

urlpatterns = [
    path('people', views.people, name='people'),
    path('person/<str:id>/', views.person, name='person'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload')
]