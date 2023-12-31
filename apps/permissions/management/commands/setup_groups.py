from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from permissions.roles_permissions import (
    customers_permissions,
    sellers_permissions,
    moderators_permissions,
    admins_permissions
)


class Command(BaseCommand):
    help = 'Assigns permissions to groups'

    def add_permissions_to_group(self, group_name: str, permissions_set):
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(codename__in=permissions_set)
        group.permissions.set(permissions)

    def handle(self, *args, **options):
        self.stdout.write('Setting default users groups...')
        self.add_permissions_to_group('Customers', customers_permissions)
        self.add_permissions_to_group('Sellers', sellers_permissions)
        self.add_permissions_to_group('Moderators', moderators_permissions)
        self.add_permissions_to_group('Admins', admins_permissions)
        self.stdout.write(self.style.SUCCESS('Done setting default users roles'))
