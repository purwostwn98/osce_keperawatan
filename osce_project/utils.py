from django.contrib.admin.models import LogEntry
from django.db.models import Count
from master.models import Mahasiswa, Dosen, BankSoal
from ujian.models import JadwalUjian
from alokasi.models import AlokasiMahasiswa, AlokasiDosen
from penilaian.models import NilaiMahasiswa


def environment_callback(request):
    """Return environment info for Unfold admin"""
    return ["OSCE Keperawatan", "Production"]


def dashboard_callback(request, context):
    """Dashboard data for Unfold admin"""
    return [
        {
            "title": "Total Mahasiswa",
            "metric": Mahasiswa.objects.count(),
            "footer": "Total mahasiswa terdaftar",
            "chart": {
                "type": "bar",
                "data": {
                    "labels": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"],
                    "datasets": [
                        {
                            "label": "Mahasiswa Baru",
                            "data": [12, 19, 3, 5, 2, 3],
                            "backgroundColor": "rgba(54, 162, 235, 0.2)",
                            "borderColor": "rgba(54, 162, 235, 1)",
                            "borderWidth": 1,
                        }
                    ],
                },
                "options": {
                    "responsive": True,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                        }
                    },
                },
            },
        },
        {
            "title": "Total Dosen",
            "metric": Dosen.objects.count(),
            "footer": "Dosen aktif",
        },
        {
            "title": "Bank Soal",
            "metric": BankSoal.objects.count(),
            "footer": "Total bank soal tersedia",
        },
        {
            "title": "Jadwal Ujian Aktif",
            "metric": JadwalUjian.objects.filter(status=True).count(),
            "footer": "Ujian yang sedang berlangsung",
        },
        {
            "title": "Mahasiswa Teralokasi",
            "metric": AlokasiMahasiswa.objects.count(),
            "footer": "Mahasiswa yang sudah dialokasikan",
        },
        {
            "title": "Dosen Teralokasi",
            "metric": AlokasiDosen.objects.count(),
            "footer": "Dosen yang sudah dialokasikan",
        },
        {
            "title": "Total Nilai",
            "metric": NilaiMahasiswa.objects.count(),
            "footer": "Total penilaian yang sudah diinput",
        },
        {
            "title": "Recent Activities",
            "metric": "",
            "footer": "Aktivitas terbaru",
            "chart": {
                "type": "line",
                "data": {
                    "labels": ["7 hari lalu", "6 hari lalu", "5 hari lalu", "4 hari lalu", "3 hari lalu", "2 hari lalu", "Kemarin"],
                    "datasets": [
                        {
                            "label": "Admin Actions",
                            "data": list(
                                LogEntry.objects.extra(
                                    select={"day": "date(action_time)"}
                                )
                                .values("day")
                                .annotate(count=Count("id"))
                                .order_by("-day")[:7]
                                .values_list("count", flat=True)
                            )[::-1],
                            "backgroundColor": "rgba(255, 99, 132, 0.2)",
                            "borderColor": "rgba(255, 99, 132, 1)",
                            "borderWidth": 2,
                        }
                    ],
                },
                "options": {
                    "responsive": True,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                        }
                    },
                },
            },
        },
    ]
