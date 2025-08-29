from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

# Register your models here.
from .models import JadwalUjian, AspekUjian, KelompokUjian


class AspekUjianInline(TabularInline):
    model = AspekUjian
    extra = 0
    fields = ['aspek', 'bobot', 'order', 'durasi']
    ordering = ['order']


class KelompokUjianInline(TabularInline):
    model = KelompokUjian
    extra = 0
    fields = ['nama_kelompok']


@admin.register(JadwalUjian)
class JadwalUjianAdmin(ModelAdmin):
    list_display = ['bank_soal', 'semester_akademik', 'kode_mk', 'status', 'start_date', 'end_date']
    search_fields = ['bank_soal__nama_soal', 'kode_mk']
    list_filter = ['status', 'semester_akademik', 'start_date', 'created_at']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AspekUjianInline, KelompokUjianInline]
    
    fieldsets = [
        ('Informasi Ujian', {
            'fields': ['bank_soal', 'semester_akademik', 'kode_mk', 'status']
        }),
        ('Jadwal', {
            'fields': ['start_date', 'end_date']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    @display(description="Duration", ordering="start_date")
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            delta = obj.end_date - obj.start_date
            return f"{delta.days} hari"
        return "-"


@admin.register(AspekUjian)
class AspekUjianAdmin(ModelAdmin):
    list_display = ['jadwal_ujian', 'aspek', 'bobot', 'order', 'durasi']
    search_fields = ['jadwal_ujian__bank_soal__nama_soal', 'aspek__aspek']
    list_filter = ['jadwal_ujian', 'bobot', 'created_at']
    ordering = ['jadwal_ujian', 'order']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Aspek', {
            'fields': ['jadwal_ujian', 'aspek', 'bobot', 'order', 'durasi']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(KelompokUjian)
class KelompokUjianAdmin(ModelAdmin):
    list_display = ['jadwal_ujian', 'nama_kelompok', 'created_at']
    search_fields = ['jadwal_ujian__bank_soal__nama_soal', 'nama_kelompok']
    list_filter = ['jadwal_ujian', 'created_at']
    ordering = ['jadwal_ujian', 'nama_kelompok']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informasi Kelompok', {
            'fields': ['jadwal_ujian', 'nama_kelompok']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

