def environment_callback(request):
    """Return environment info for Unfold admin"""
    return ["OSCE Keperawatan", "Production"]


def dashboard_callback(request, context):
    """Dashboard data for Unfold admin - Hardcoded for now"""
    return {
        "kpis": [
            {
                "title": "Total Mahasiswa",
                "metric": 125,
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
                "metric": 25,
                "footer": "Dosen aktif",
            },
            {
                "title": "Bank Soal",
                "metric": 45,
                "footer": "Total bank soal tersedia",
            },
            {
                "title": "Jadwal Ujian Aktif",
                "metric": 3,
                "footer": "Ujian yang sedang berlangsung",
            },
            {
                "title": "Mahasiswa Teralokasi",
                "metric": 98,
                "footer": "Mahasiswa yang sudah dialokasikan",
            },
            {
                "title": "Dosen Teralokasi",
                "metric": 20,
                "footer": "Dosen yang sudah dialokasikan",
            },
            {
                "title": "Total Nilai",
                "metric": 234,
                "footer": "Total penilaian yang sudah diinput",
            },
            {
                "title": "Recent Activities",
                "metric": "8",
                "footer": "Aktivitas terbaru",
                "chart": {
                    "type": "line",
                    "data": {
                        "labels": ["7 hari lalu", "6 hari lalu", "5 hari lalu", "4 hari lalu", "3 hari lalu", "2 hari lalu", "Kemarin"],
                        "datasets": [
                            {
                                "label": "Admin Actions",
                                "data": [2, 5, 3, 8, 1, 4, 6],
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
    }
