# relationship_app/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **options):
        # Define groups
        groups_permissions = {
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
            'Editors': ['can_create', 'can_edit', 'can_view'],
            'Viewers': ['can_view'],
        }

        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_code in perms:
                perm = Permission.objects.get(codename=perm_code, content_type__app_label='relationship_app')
                group.permissions.add(perm)
            group.save()

        self.stdout.write(self.style.SUCCESS('Groups and permissions successfully created'))

