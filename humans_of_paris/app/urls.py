from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cluster', views.cluster, name='cluster'),
    path('yourdoppelganger', views.yourdoppelganger, name='yourdoppelganger'),
    path('record/<str:id>/', views.record, name='record'),
    path('person_records/<str:name>/', views.person_records, name='person_records'),
    path('upload', views.upload, name='upload')
]
# + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT)