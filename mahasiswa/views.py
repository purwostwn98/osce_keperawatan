from django.shortcuts import render

# Create your views here.
def index_mahasiswa(request):
    context = {
        'menu' : ['home', '']
    }
    return render(request, 'mahasiswa/index_mahasiswa.html', context)

def jadwal_ujian(request):
    context = {
        'menu' : ['osce', 'jadwal_ujian']
    }
    return render(request, 'mahasiswa/ujian_osce/jadwal_ujian.html', context)
