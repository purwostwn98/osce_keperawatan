from django.shortcuts import render
from django.urls import reverse

def pdfjs_page(request, filename):
    pdf_url = reverse("pdf_view", args=[filename])  # from option #1
    return render(request, "template_pdfjs.html", {"pdf_url": pdf_url})
