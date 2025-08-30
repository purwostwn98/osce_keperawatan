from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_mahasiswa, name='index_mahasiswa'),
    path('jadwal/', views.jadwal_ujian, name='jadwal_ujian')
]
