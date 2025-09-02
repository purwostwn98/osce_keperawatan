from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Group
from django.dispatch import receiver
from master.models import Dosen, Mahasiswa

@receiver(user_logged_in)
def assign_user_group(sender, request, user, **kwargs):
    """
    Automatically assign users to appropriate groups based on their profile
    """
    # Only process for CAS-authenticated users
    if hasattr(request, 'session') and request.session.get('_auth_user_backend') == 'django_cas_ng.backends.CASBackend':
        try:
            # Check if user is a dosen
            if Dosen.objects.filter(user=user).exists():
                group, created = Group.objects.get_or_create(name='dosen')
                user.groups.add(group)
                
            # Check if user is a mahasiswa  
            elif Mahasiswa.objects.filter(user=user).exists():
                group, created = Group.objects.get_or_create(name='mahasiswa')
                user.groups.add(group)
                
        except Exception as e:
            # Log error but don't break login process
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error assigning group to user {user.username}: {e}")
