from django.urls import path
from . import views

app_name = 'master'

urlpatterns = [
    path('sync-dosen/', views.sync_dosen_view, name='sync_dosen'),
    path('sync-mahasiswa/', views.sync_mahasiswa_view, name='sync_mahasiswa'),
    path('get-mahasiswa-profile/', views.get_mahasiswa_profile_view, name='get_mahasiswa_profile'),
]
