from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('facemap', views.cluster, name='facemap'),
    path('yourdoppelganger', views.yourdoppelganger, name='yourdoppelganger'),
    path('record/<str:id>/', views.record, name='record'),
]
# + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT)