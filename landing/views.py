from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'landing/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    else: 
        return render(request, 'landing/login.html')

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

def cas_callback(request):
    """
    Handle post-CAS login callback
    """
    if request.user.is_authenticated:
        return dashboard_redirect(request)
    else:
        messages.error(request, 'Login gagal. Silakan coba lagi.')
        return redirect('/')
