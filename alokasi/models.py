from django.db import models

# Create your models here.
from master.models import Mahasiswa
from ujian.models import JadwalUjian

class AlokasiMahasiswa(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    jadwal_ujian = models.ForeignKey(JadwalUjian, on_delete=models.CASCADE)
    kelompok_ujian = models.ForeignKey('ujian.KelompokUjian', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mahasiswa.nama_mahasiswa} - {self.jadwal_ujian.bank_soal.nama_soal} - {self.kelompok_ujian.nama_kelompok if self.kelompok_ujian else 'Unassigned'}"
    

class AlokasiDosen(models.Model):
    dosen = models.ForeignKey('master.Dosen', on_delete=models.CASCADE)
    jadwal_ujian = models.ForeignKey(JadwalUjian, on_delete=models.CASCADE)
    kelompok_ujian = models.ForeignKey('ujian.KelompokUjian', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dosen.nama_dosen} - {self.jadwal_ujian.bank_soal.nama_soal} - {self.kelompok_ujian.nama_kelompok if self.kelompok_ujian else 'Unassigned'}"

