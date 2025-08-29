from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

# Register your models here.
from .models import AlokasiMahasiswa, AlokasiDosen


@admin.register(AlokasiMahasiswa)
class AlokasiMahasiswaAdmin(ModelAdmin):
    list_display = ['mahasiswa', 'jadwal_ujian', 'kelompok_ujian', 'created_at']
    search_fields = ['mahasiswa__nama_mahasiswa', 'mahasiswa__nim', 'jadwal_ujian__bank_soal__nama_soal']
    list_filter = ['jadwal_ujian', 'kelompok_ujian', 'created_at']
    ordering = ['jadwal_ujian', 'kelompok_ujian', 'mahasiswa__nama_mahasiswa']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Alokasi', {
            'fields': ['mahasiswa', 'jadwal_ujian', 'kelompok_ujian']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    @display(description="NIM", ordering="mahasiswa__nim")
    def get_nim(self, obj):
        return obj.mahasiswa.nim

    @display(description="Program Studi", ordering="mahasiswa__program_studi")
    def get_prodi(self, obj):
        return obj.mahasiswa.program_studi.nama_prodi


@admin.register(AlokasiDosen)
class AlokasiDosenAdmin(ModelAdmin):
    list_display = ['dosen', 'jadwal_ujian', 'kelompok_ujian', 'created_at']
    search_fields = ['dosen__nama_dosen', 'dosen__nik', 'jadwal_ujian__bank_soal__nama_soal']
    list_filter = ['jadwal_ujian', 'kelompok_ujian', 'created_at']
    ordering = ['jadwal_ujian', 'kelompok_ujian', 'dosen__nama_dosen']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Alokasi', {
            'fields': ['dosen', 'jadwal_ujian', 'kelompok_ujian']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    @display(description="NIK", ordering="dosen__nik")
    def get_nik(self, obj):
        return obj.dosen.nik

    @display(description="Email", ordering="dosen__email")
    def get_email(self, obj):
        return obj.dosen.email
