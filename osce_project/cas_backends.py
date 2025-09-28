import logging
from django_cas_ng.backends import CASBackend
from django.contrib.auth.models import User
from django.conf import settings
import urllib.request
import urllib.parse
import ssl
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class CustomCASBackend(CASBackend):
    """Custom CAS Backend with enhanced debugging and proper verification"""
    
    def authenticate(self, request, ticket, service, **kwargs):
        """Authenticate user with custom verification only"""
        logger.info(f"CAS Authentication attempt - Service: {service}, Ticket: {ticket}")
        
        try:
            # Use only custom verification to avoid double ticket usage
            user = self._custom_verify_and_create_user(ticket, service)
            if user:
                logger.info(f"CAS Authentication successful for user: {user.username}")
            else:
                logger.warning(f"CAS Authentication failed")
                
            return user
        except Exception as e:
            logger.error(f"CAS Authentication error: {str(e)}")
            return None
    
    def _custom_verify_and_create_user(self, ticket, service):
        """Custom ticket verification with detailed logging"""
        logger.info(f"Custom verification - Service: {service}, Ticket: {ticket}")
        
        # Build verification URL
        verify_url = f"{settings.CAS_SERVER_URL}serviceValidate"
        params = {
            'service': service,
            'ticket': ticket
        }
        
        full_url = f"{verify_url}?{urllib.parse.urlencode(params)}"
        logger.info(f"Verification URL: {full_url}")
        
        try:
            # Create SSL context that doesn't verify certificates (for testing only)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Make request to CAS server
            request = urllib.request.Request(full_url)
            with urllib.request.urlopen(request, context=ssl_context) as response:
                response_data = response.read().decode('utf-8')
                logger.info(f"CAS Server Response: {response_data}")
                
                # Parse XML response
                root = ET.fromstring(response_data)
                
                # Check for success
                success_elem = root.find('.//{http://www.yale.edu/tp/cas}authenticationSuccess')
                if success_elem is not None:
                    user_elem = success_elem.find('.//{http://www.yale.edu/tp/cas}user')
                    if user_elem is not None:
                        username = user_elem.text
                        logger.info(f"CAS verification successful for user: {username}")
                        
                        # Get or create user
                        user, created = User.objects.get_or_create(username=username)
                        if created:
                            logger.info(f"Created new user: {username}")
                            # Set basic user info
                            user.first_name = username
                            user.email = f"{username}@ums.ac.id"
                            user.save()
                        
                        return user
                
                # Check for failure
                failure_elem = root.find('.//{http://www.yale.edu/tp/cas}authenticationFailure')
                if failure_elem is not None:
                    error_code = failure_elem.get('code', 'Unknown')
                    error_msg = failure_elem.text or 'No error message'
                    logger.error(f"CAS verification failed - Code: {error_code}, Message: {error_msg}")
                
                return None
                
        except Exception as e:
            logger.error(f"Error during custom CAS verification: {str(e)}")
            return None
