from django.contrib import admin

# Register your models here.
from .models import Fakultas, ProgramStudi, Mahasiswa, Dosen, KategoriSoal, BankAspekPenilaian, BankSoal, SemesterAkademik

admin.site.register(Fakultas)
admin.site.register(ProgramStudi)
admin.site.register(Mahasiswa)
admin.site.register(Dosen)
admin.site.register(KategoriSoal)
admin.site.register(BankAspekPenilaian)
admin.site.register(BankSoal)
admin.site.register(SemesterAkademik)
