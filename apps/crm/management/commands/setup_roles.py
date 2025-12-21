from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


ROLE_PERMISSIONS = {
    "Admin": {
        "orders": ["add", "change", "delete", "view"],
        "catalog": ["add", "change", "delete", "view"],
        "crm": ["add", "change", "delete", "view"],
    },
    "Operator": {
        "orders": ["add", "change", "view"],
        "catalog": ["view"],
        "crm": ["view"],
    },
    "Courier": {
        "orders": ["view", "change"],
        "crm": ["view"],
    },
}


class Command(BaseCommand):
    help = "Create default CRM roles (Admin, Operator, Courier) with basic permissions."

    def handle(self, *args, **options):
        for role, app_permissions in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=role)
            perms = []
            for app_label, actions in app_permissions.items():
                for action in actions:
                    perms.extend(
                        Permission.objects.filter(codename__startswith=f"{action}_", content_type__app_label=app_label)
                    )
            group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f"Rol yaratildi: {role} ({len(perms)} ta ruxsat)"))
