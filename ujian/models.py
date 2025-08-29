from django.db import models

# Create your models here.
from master.models import BankSoal

class JadwalUjian(models.Model):
    bank_soal = models.ForeignKey(BankSoal, on_delete=models.CASCADE)
    semester_akademik = models.ForeignKey('master.SemesterAkademik', on_delete=models.CASCADE)
    kode_mk = models.CharField(max_length=10)
    status = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_soal.nama_soal} - {self.semester_akademik.nama_semester}"
    
class AspekUjian(models.Model):
    jadwal_ujian = models.ForeignKey(JadwalUjian, on_delete=models.CASCADE)
    aspek = models.ForeignKey('master.BankAspekPenilaian', on_delete=models.CASCADE)
    bobot = models.IntegerField()
    order = models.IntegerField()
    durasi = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.jadwal_ujian.bank_soal.nama_soal} - {self.aspek.aspek}"
    
class KelompokUjian(models.Model):
    jadwal_ujian = models.ForeignKey(JadwalUjian, on_delete=models.CASCADE)
    nama_kelompok = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.jadwal_ujian.bank_soal.nama_soal} - {self.nama_kelompok}"
