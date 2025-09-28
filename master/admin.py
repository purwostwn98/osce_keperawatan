from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .views import sync_dosen_view, sync_mahasiswa_view

# Register your models here.
from .models import Fakultas, ProgramStudi, Mahasiswa, Dosen, KategoriSoal, BankAspekPenilaian, BankSoal, SemesterAkademik


@admin.register(Fakultas)
class FakultasAdmin(ModelAdmin):
    list_display = ['id_lembaga', 'nama_fakultas']
    search_fields = ['id_lembaga', 'nama_fakultas']
    list_filter = ['id_lembaga']
    ordering = ['nama_fakultas']
    
    fieldsets = [
        ('Informasi Fakultas', {
            'fields': ['id_lembaga', 'nama_fakultas']
        }),
    ]


class ProgramStudiInline(TabularInline):
    model = ProgramStudi
    extra = 0
    fields = ['id_lembaga', 'nama_prodi', 'kode_prodi', 'fid']


@admin.register(ProgramStudi)
class ProgramStudiAdmin(ModelAdmin):
    list_display = ['id_lembaga', 'nama_prodi', 'kode_prodi', 'fakultas_id', 'fid']
    search_fields = ['id_lembaga', 'nama_prodi', 'kode_prodi']
    list_filter = ['fakultas_id']
    ordering = ['nama_prodi']
    
    fieldsets = [
        ('Informasi Program Studi', {
            'fields': ['id_lembaga', 'nama_prodi', 'kode_prodi', 'fakultas_id', 'fid']
        }),
    ]


@admin.register(Mahasiswa)
class MahasiswaAdmin(ModelAdmin):
    list_display = ['nim', 'nama_mahasiswa', 'program_studi', 'semester', 'angkatan', 'email']
    search_fields = ['nim', 'nama_mahasiswa', 'email']
    list_filter = ['program_studi', 'semester', 'angkatan']
    ordering = ['nama_mahasiswa']
    
    fieldsets = [
        ('Informasi Akademik', {
            'fields': ['nim', 'nama_mahasiswa', 'program_studi', 'semester', 'angkatan']
        }),
        ('Kontak', {
            'fields': ['email', 'no_hp', 'alamat']
        }),
    ]
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-mahasiswa/', self.admin_site.admin_view(sync_mahasiswa_view), name='master_mahasiswa_sync'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        """
        Override changelist view untuk menambahkan tombol sync dan dropdown tahun angkatan
        """
        import datetime
        extra_context = extra_context or {}
        extra_context['sync_url'] = reverse('admin:master_mahasiswa_sync')
        # Dropdown tahun angkatan: 5 tahun terakhir dari tahun sekarang
        current_year = datetime.datetime.now().year
        extra_context['angkatan_years'] = [str(current_year - i) for i in range(10)]
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Dosen)
class DosenAdmin(ModelAdmin):
    list_display = ['nik', 'uniid', 'nama_dosen', 'email', 'created_at']
    search_fields = ['nik', 'uniid', 'nama_dosen', 'email']
    list_filter = ['created_at']
    ordering = ['nama_dosen']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Dosen', {
            'fields': ['nik', 'uniid', 'nama_dosen', 'email']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-dosen/', self.admin_site.admin_view(sync_dosen_view), name='master_dosen_sync'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        """
        Override changelist view untuk menambahkan tombol sync
        """
        extra_context = extra_context or {}
        extra_context['sync_url'] = reverse('admin:master_dosen_sync')
        return super().changelist_view(request, extra_context=extra_context)


class BankAspekPenilaianInline(TabularInline):
    model = BankAspekPenilaian
    extra = 0
    fields = ['aspek', 'status']


@admin.register(KategoriSoal)
class KategoriSoalAdmin(ModelAdmin):
    list_display = ['nama_kategori', 'created_at']
    search_fields = ['nama_kategori']
    list_filter = ['created_at']
    ordering = ['nama_kategori']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BankAspekPenilaianInline]
    
    fieldsets = [
        ('Informasi Kategori', {
            'fields': ['nama_kategori']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(BankAspekPenilaian)
class BankAspekPenilaianAdmin(ModelAdmin):
    list_display = ['aspek', 'kategori', 'status', 'created_at']
    search_fields = ['aspek']
    list_filter = ['kategori', 'status', 'created_at']
    ordering = ['kategori', 'aspek']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Aspek', {
            'fields': ['kategori', 'aspek', 'status']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(BankSoal)
class BankSoalAdmin(ModelAdmin):
    list_display = ['nama_soal', 'nama_file', 'created_at']
    search_fields = ['nama_soal', 'nama_file']
    list_filter = ['created_at']
    ordering = ['nama_soal']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Soal', {
            'fields': ['nama_soal', 'nama_file']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(SemesterAkademik)
class SemesterAkademikAdmin(ModelAdmin):
    list_display = ['kode_semester', 'nama_semester', 'order']
    search_fields = ['kode_semester', 'nama_semester']
    list_filter = ['order']
    ordering = ['order']
    
    fieldsets = [
        ('Informasi Semester', {
            'fields': ['kode_semester', 'nama_semester', 'order']
        }),
    ]
