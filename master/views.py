from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from decouple import config
import requests
import logging
from .models import Dosen
from .utils import APIClient, validate_dosen_data, normalize_dosen_data


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

