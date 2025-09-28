from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create user groups for OSCE system'

    def handle(self, *args, **options):
        # Create groups
        dosen_group, created = Group.objects.get_or_create(name='dosen')
        mahasiswa_group, created = Group.objects.get_or_create(name='mahasiswa')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created group: {dosen_group.name}')
            )
        else:
            self.stdout.write(f'Group already exists: {dosen_group.name}')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created group: {mahasiswa_group.name}')
            )
        else:
            self.stdout.write(f'Group already exists: {mahasiswa_group.name}')

        self.stdout.write(
            self.style.SUCCESS('User groups setup completed!')
        )
