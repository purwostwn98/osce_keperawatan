from django.urls import path
from . import views

app_name = 'master'

urlpatterns = [
    path('sync-dosen/', views.sync_dosen_view, name='sync_dosen'),
]
