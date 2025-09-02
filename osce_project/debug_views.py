from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def cas_debug(request):
    """Debug endpoint untuk CAS configuration"""
    debug_info = {
        'CAS_SERVER_URL': settings.CAS_SERVER_URL,
        'CAS_VERSION': settings.CAS_VERSION,
        'LOGIN_URL': settings.LOGIN_URL,
        'LOGIN_REDIRECT_URL': settings.LOGIN_REDIRECT_URL,
        'current_request_url': request.build_absolute_uri(),
        'service_url': request.build_absolute_uri(reverse('cas_ng_login')),
        'full_cas_login_url': f"{settings.CAS_SERVER_URL}login?service={request.build_absolute_uri(reverse('cas_ng_login'))}",
        'request_params': dict(request.GET.items()),
        'authentication_backends': settings.AUTHENTICATION_BACKENDS,
    }
    
    logger.info(f"CAS Debug Info: {debug_info}")
    return JsonResponse(debug_info, indent=2)
