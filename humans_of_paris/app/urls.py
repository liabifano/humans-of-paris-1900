from django.urls import path
from django.conf.urls.static import static

from . import views
from humans_of_paris.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT

urlpatterns = [
    path('people', views.people, name='people'),
    path('record/<str:id>/', views.record, name='record'),
    path('person_records/<str:name>/', views.person_records, name='person_records'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload')
] + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT)