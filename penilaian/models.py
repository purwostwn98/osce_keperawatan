from django.db import models

# Create your models here.
class NilaiMahasiswa(models.Model):
    mahasiswa = models.ForeignKey('master.Mahasiswa', on_delete=models.CASCADE)
    aspek_ujian = models.ForeignKey('ujian.AspekUjian', on_delete=models.CASCADE)
    skor = models.DecimalField(max_digits=5, decimal_places=2)
    tanggal_penilaian = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.aspek_ujian.nama_aspek}"