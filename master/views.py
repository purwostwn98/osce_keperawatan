from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from decouple import config
import requests
import logging
from .models import Dosen, Mahasiswa, ProgramStudi
from .utils import APIClient, validate_dosen_data, normalize_dosen_data, validate_mahasiswa_data, normalize_mahasiswa_data


# Set up logging
logger = logging.getLogger(__name__)

def sync_dosen_data():
    """
    Fungsi utama untuk sinkronisasi data dosen dari API
    Melakukan upsert data ke database
    """
    success_count = 0
    updated_count = 0
    created_count = 0
    
    try:
        # Initialize API client
        api_client = APIClient()
        
        # Get dosen data from API
        api_dosen_data = api_client.get_dosen_data()
        if not api_dosen_data:
            return {
                'status': 'error',
                'message': 'No data received from API or failed to get API token',
                'data': {
                    'success_count': 0,
                    'created_count': 0,
                    'updated_count': 0
                }
            }
        
        # Process data and upsert to database
        with transaction.atomic():
            for dosen_data in api_dosen_data:
                try:
                    # Validate data
                    if not validate_dosen_data(dosen_data):
                        logger.warning(f"Invalid data format: {dosen_data}")
                        continue
                    
                    # Normalize data
                    normalized_data = normalize_dosen_data(dosen_data)
                    
                    # Upsert data dosen
                    dosen, created = Dosen.objects.update_or_create(
                        nik=normalized_data['nik'],
                        defaults={
                            'uniid': normalized_data['uniid'],
                            'nama_dosen': normalized_data['nama_dosen'],
                            'email': normalized_data['email']
                        }
                    )
                    
                    if created:
                        created_count += 1
                        logger.info(f"Created new dosen: {dosen.nama_dosen}")
                    else:
                        updated_count += 1
                        logger.info(f"Updated dosen: {dosen.nama_dosen}")
                    
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing dosen data {dosen_data}: {e}")
                    continue
        
        return {
            'status': 'success',
            'message': f'Sync completed: {created_count} created, {updated_count} updated',
            'data': {
                'success_count': success_count,
                'created_count': created_count,
                'updated_count': updated_count
            }
        }
        
    except Exception as e:
        logger.error(f"Critical error during sync: {e}")
        return {
            'status': 'error',
            'message': f'Critical error during sync: {str(e)}',
            'data': {
                'success_count': success_count,
                'created_count': created_count,
                'updated_count': updated_count
            }
        }

def sync_dosen_view(request):
    """
    View function untuk handle sync dosen data
    Mendukung AJAX request dari admin interface
    """
    if request.method == 'POST':
        result = sync_dosen_data()
        
        # Untuk AJAX request, return JSON response
        if request.headers.get('Content-Type') == 'application/json' or request.META.get('HTTP_ACCEPT', '').find('application/json') != -1:
            return JsonResponse(result)
        
        # Untuk request biasa, set messages dan redirect
        if result['status'] == 'success':
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
        
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(reverse('admin:master_dosen_changelist'))
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def sync_mahasiswa_data():
    """
    Fungsi utama untuk sinkronisasi data mahasiswa dari API
    Melakukan upsert data ke database
    """
    success_count = 0
    updated_count = 0
    created_count = 0
    
    try:
        # Initialize API client
        api_client = APIClient()
        
        # Get mahasiswa data from API
        api_mahasiswa_data = api_client.get_mahasiswa_data()
        if not api_mahasiswa_data:
            return {
                'status': 'error',
                'message': 'No mahasiswa data received from API or failed to get API token',
                'data': {
                    'success_count': 0,
                    'created_count': 0,
                    'updated_count': 0
                }
            }
        
        # Process data and upsert to database
        with transaction.atomic():
            for mahasiswa_data in api_mahasiswa_data:
                try:
                    # Validate data
                    if not validate_mahasiswa_data(mahasiswa_data):
                        logger.warning(f"Invalid mahasiswa data format: {mahasiswa_data}")
                        continue
                    
                    # Normalize data
                    normalized_data = normalize_mahasiswa_data(mahasiswa_data)
                    
                    # Cari program studi berdasarkan kode atau nama prodi
                    program_studi = None
                    if 'prodi' in normalized_data:
                        try:
                            # Coba cari berdasarkan kode prodi terlebih dahulu
                            program_studi = ProgramStudi.objects.filter(
                                kode_prodi__icontains=normalized_data['prodi']
                            ).first()
                            
                            # Jika tidak ditemukan, coba cari berdasarkan nama prodi
                            if not program_studi:
                                program_studi = ProgramStudi.objects.filter(
                                    nama_prodi__icontains=normalized_data['prodi']
                                ).first()
                        except Exception as e:
                            logger.warning(f"Error finding program studi for {normalized_data['prodi']}: {e}")
                    
                    # Skip jika program studi tidak ditemukan
                    if not program_studi:
                        logger.warning(f"Program studi not found for mahasiswa {normalized_data['nim']}: {normalized_data.get('prodi', 'N/A')}")
                        continue
                    
                    # Upsert data mahasiswa
                    mahasiswa, created = Mahasiswa.objects.update_or_create(
                        nim=normalized_data['nim'],
                        defaults={
                            'nama_mahasiswa': normalized_data['nama_mahasiswa'],
                            'program_studi': program_studi,
                            'semester': normalized_data.get('semester', 1),
                            'angkatan': normalized_data.get('angkatan', 2024),
                            'email': normalized_data.get('email', ''),
                            'no_hp': normalized_data.get('no_hp', ''),
                            'alamat': normalized_data.get('alamat', '')
                        }
                    )
                    
                    if created:
                        created_count += 1
                        logger.info(f"Created new mahasiswa: {mahasiswa.nama_mahasiswa}")
                    else:
                        updated_count += 1
                        logger.info(f"Updated mahasiswa: {mahasiswa.nama_mahasiswa}")
                    
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing mahasiswa data {mahasiswa_data}: {e}")
                    continue
        
        return {
            'status': 'success',
            'message': f'Mahasiswa sync completed: {created_count} created, {updated_count} updated',
            'data': {
                'success_count': success_count,
                'created_count': created_count,
                'updated_count': updated_count
            }
        }
        
    except Exception as e:
        logger.error(f"Critical error during mahasiswa sync: {e}")
        return {
            'status': 'error',
            'message': f'Critical error during mahasiswa sync: {str(e)}',
            'data': {
                'success_count': success_count,
                'created_count': created_count,
                'updated_count': updated_count
            }
        }

def sync_mahasiswa_view(request):
    """
    View function untuk handle sync mahasiswa data
    Mendukung AJAX request dari admin interface
    """
    if request.method == 'POST':
        # Ambil parameter dari form POST
        prodi = request.POST.get('prodi')
        angkatan = request.POST.get('angkatan')
        # Jalankan sinkronisasi dengan parameter
        def sync_mahasiswa_data_with_param(prodi, angkatan):
            success_count = 0
            updated_count = 0
            created_count = 0
            try:
                api_client = APIClient()
                api_mahasiswa_data = api_client.get_mahasiswa_data(prodi=prodi, angkatan=angkatan)
                if not api_mahasiswa_data:
                    return {
                        'status': 'error',
                        'message': 'No mahasiswa data received from API or failed to get API token',
                        'data': {
                            'success_count': 0,
                            'created_count': 0,
                            'updated_count': 0
                        }
                    }
                from django.db import transaction
                with transaction.atomic():
                    for mahasiswa_data in api_mahasiswa_data:
                        try:
                            if not validate_mahasiswa_data(mahasiswa_data):
                                continue
                            normalized_data = normalize_mahasiswa_data(mahasiswa_data)
                            program_studi = None
                            if 'prodi' in normalized_data:
                                try:
                                    program_studi = ProgramStudi.objects.filter(kode_prodi__icontains=normalized_data['prodi']).first()
                                    if not program_studi:
                                        program_studi = ProgramStudi.objects.filter(nama_prodi__icontains=normalized_data['prodi']).first()
                                except Exception:
                                    pass
                            if not program_studi:
                                continue
                            mahasiswa, created = Mahasiswa.objects.update_or_create(
                                nim=normalized_data['nim'],
                                defaults={
                                    'nama_mahasiswa': normalized_data['nama_mahasiswa'],
                                    'program_studi': program_studi,
                                    'semester': normalized_data.get('semester', 1),
                                    'angkatan': normalized_data.get('angkatan', 2024),
                                    'email': normalized_data.get('email', ''),
                                    'no_hp': normalized_data.get('no_hp', ''),
                                    'alamat': normalized_data.get('alamat', '')
                                }
                            )
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                            success_count += 1
                        except Exception:
                            continue
                return {
                    'status': 'success',
                    'message': f'Mahasiswa sync completed: {created_count} created, {updated_count} updated',
                    'data': {
                        'success_count': success_count,
                        'created_count': created_count,
                        'updated_count': updated_count
                    }
                }
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Critical error during mahasiswa sync: {str(e)}',
                    'data': {
                        'success_count': success_count,
                        'created_count': created_count,
                        'updated_count': updated_count
                    }
                }
        result = sync_mahasiswa_data_with_param(prodi, angkatan)
        # Untuk AJAX request, return JSON response
        if request.headers.get('Content-Type') == 'application/json' or request.META.get('HTTP_ACCEPT', '').find('application/json') != -1 or request.content_type.startswith('multipart/form-data'):
            return JsonResponse(result)
        # Untuk request biasa, set messages dan redirect
        if result['status'] == 'success':
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(reverse('admin:master_mahasiswa_changelist'))
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def get_mahasiswa_profile_view(request):
    """
    View function untuk mendapatkan profil mahasiswa berdasarkan NIM
    """
    if request.method == 'POST':
        nim = request.POST.get('nim')
        session_cookie = request.POST.get('session_cookie')
        
        if not nim:
            return JsonResponse({
                'status': 'error',
                'message': 'NIM is required'
            }, status=400)
        
        try:
            # Initialize API client
            api_client = APIClient()
            
            # Get mahasiswa profile from API
            profile_data = api_client.get_mahasiswa_profile(nim, session_cookie)
            
            if profile_data:
                return JsonResponse({
                    'status': 'success',
                    'message': f'Profile retrieved for NIM: {nim}',
                    'data': profile_data
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Failed to retrieve profile for NIM: {nim}'
                }, status=404)
                
        except Exception as e:
            logger.error(f"Error in get_mahasiswa_profile_view: {e}")
            return JsonResponse({
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

