from django.db import models

# Create your models here.
class Fakultas(models.Model):
    id_lembaga = models.CharField(max_length=30, unique=True)
    nama_fakultas = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}, {self.id_lembaga} - {self.nama_fakultas}"

class ProgramStudi(models.Model):
    id_lembaga = models.CharField(max_length=30, unique=True)
    nama_prodi = models.CharField(max_length=255)
    fakultas_id = models.ForeignKey(Fakultas, on_delete=models.CASCADE)
    kode_prodi = models.CharField(max_length=10, unique=True)
    fid = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.id_lembaga} - {self.nama_prodi} - {self.fakultas_id}"

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=10, unique=True)
    nama_mahasiswa = models.CharField(max_length=255)
    program_studi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE)
    semester = models.IntegerField()
    angkatan = models.IntegerField()
    no_hp = models.CharField(max_length=15, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.nim} - {self.nama_mahasiswa} - {self.program_studi}"
    
class Dosen(models.Model):
    nik = models.CharField(max_length=18, unique=True)
    uniid = models.CharField(max_length=10, unique=True)
    nama_dosen = models.CharField(max_length=255) 
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nik} - {self.nama_dosen}"
    
class KategoriSoal(models.Model):
    nama_kategori = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_kategori}"

class BankAspekPenilaian(models.Model):
    kategori = models.ForeignKey(KategoriSoal, on_delete=models.CASCADE)
    aspek = models.TextField(null=False, blank=False)  
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aspek}"
    
class BankSoal(models.Model):
    nama_soal = models.CharField(max_length=255)
    nama_file = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_soal}"
    
class SemesterAkademik(models.Model):
    kode_semester = models.CharField(max_length=10, unique=True)
    nama_semester = models.CharField(max_length=255)
    order = models.IntegerField()

