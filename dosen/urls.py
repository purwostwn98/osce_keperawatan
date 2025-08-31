from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index_dosen, name='index_dosen'),
    path('jadwal/', views.jadwal_ujian_dosen, name='jadwal_ujian_dosen'),
    path('detail/', views.detail_ujian_dosen, name='detail_ujian_dosen'),
    path('penilaian/<int:id_mhs>/', views.penilaian_ujian_dosen, name='penilaian_ujian_dosen'),
    path("pdfs/<str:filename>/", views.pdf_view, name="pdf_view")
] 
