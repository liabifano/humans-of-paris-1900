from django.urls import path
from . import views

urlpatterns = [
    path('people', views.people, name='people'),
    path('record/<str:id>/', views.record, name='record'),
    path('person_records/<str:name>/', views.person_records, name='person_records'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload')
]