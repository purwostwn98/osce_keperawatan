from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

# Register your models here.
from .models import NilaiMahasiswa


@admin.register(NilaiMahasiswa)
class NilaiMahasiswaAdmin(ModelAdmin):
    list_display = ['mahasiswa', 'aspek_ujian', 'skor', 'tanggal_penilaian', 'updated_by']
    search_fields = ['mahasiswa__nama_mahasiswa', 'mahasiswa__nim', 'aspek_ujian__jadwal_ujian__bank_soal__nama_soal']
    list_filter = ['aspek_ujian__jadwal_ujian', 'tanggal_penilaian', 'updated_by']
    ordering = ['-tanggal_penilaian']
    readonly_fields = ['tanggal_penilaian', 'updated_at']
    
    fieldsets = [
        ('Informasi Penilaian', {
            'fields': ['mahasiswa', 'aspek_ujian', 'skor']
        }),
        ('Metadata', {
            'fields': ['updated_by', 'tanggal_penilaian', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    @display(description="NIM", ordering="mahasiswa__nim")
    def get_nim(self, obj):
        return obj.mahasiswa.nim

    @display(description="Ujian", ordering="aspek_ujian__jadwal_ujian")
    def get_ujian(self, obj):
        return obj.aspek_ujian.jadwal_ujian.bank_soal.nama_soal

    @display(description="Aspek", ordering="aspek_ujian__aspek")
    def get_aspek(self, obj):
        return obj.aspek_ujian.aspek.aspek

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
