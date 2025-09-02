from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'landing/index.html')

def login_view(request):
    """Regular login form (fallback) - redirect to CAS"""
    return redirect('cas_ng_login')

@login_required
def dashboard_redirect(request):
    """
    Redirect user to appropriate dashboard based on their role/group
    """
    user = request.user
    
    # Check if user is in dosen group
    if user.groups.filter(name='dosen').exists():
        return redirect('/dosen/')
    
    # Check if user is in mahasiswa group
    elif user.groups.filter(name='mahasiswa').exists():
        return redirect('/mahasiswa/')
    
    # Check if user is admin/staff
    elif user.is_staff or user.is_superuser:
        return redirect('/admin/')
    
    # Default redirect if no specific role is found
    else:
        messages.info(request, 'Akun Anda belum memiliki role yang sesuai. Silakan hubungi administrator.')
        return redirect('/')

def cas_login(request):
    """Redirect to CAS login"""
    return redirect('cas_ng_login')

def cas_logout(request):
    """Redirect to CAS logout"""
    return redirect('cas_ng_logout')
