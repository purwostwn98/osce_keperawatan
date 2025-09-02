from django_cas_ng.views import LoginView as CASLoginView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CustomCASLoginView(CASLoginView):
    """Custom CAS Login View with proper success handling"""
    
    def successful_login(self, request, next_page):
        """Handle successful login with proper redirect"""
        logger.info(f"Successful CAS login for user: {request.user.username}")
        
        if request.user.is_authenticated:
            # Add success message
            messages.success(request, f'Selamat datang, {request.user.username}!')
            
            # Redirect to dashboard instead of next_page
            return redirect('/dashboard/')
        
        # Fallback to standard behavior
        return super().successful_login(request, next_page)
