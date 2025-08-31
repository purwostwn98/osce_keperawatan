from django.shortcuts import render
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt
from pathlib import Path
from django.conf import settings

# Create your views here.
def index_dosen(request):
    context = {
        'menu' : ['home-dosen', '']
    }
    return render(request, 'dosen/index_dosen.html', context)

def detail_ujian_dosen(request):
    context = {
        'menu' : ['home', 'jadwal_ujian_dosen']
    }
    return render(request, 'dosen/ujian_osce/detail_ujian_dosen.html', context)

def jadwal_ujian_dosen(request):
    context = {
        'menu' : ['home', 'jadwal_ujian_dosen']
    }
    return render(request, 'dosen/ujian_osce/jadwal_ujian_dosen.html', context)

def penilaian_ujian_dosen(request, id_mhs):
    context = {
        'menu' : ['home', 'jadwal_ujian_dosen'],
        "pdf_url": "/dosen/media/pdfs/contoh_soal.pdf",
        "viewer_url" : "https://unpkg.com/pdfjs-dist@4.2.67/web/viewer.html"
    }
    return render(request, 'dosen/ujian_osce/penilaian_dosen.html', context)

@xframe_options_exempt
def pdf_view(request, filename):
    pdf_path = Path(settings.MEDIA_ROOT) / "pdfs" / filename
    if not pdf_path.exists():
        raise Http404("PDF not found")
    return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
