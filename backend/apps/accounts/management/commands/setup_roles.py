from django.core.management.base import BaseCommand
from apps.accounts.services.role_service import RoleService, ROLES


class Command(BaseCommand):
    help = "Setup enterprise roles and permissions"

    def handle(self, *args, **kwargs):
        RoleService.setup_roles()
        self.stdout.write(
            self.style.SUCCESS(f"Roles created: {', '.join(ROLES)}")
        )
