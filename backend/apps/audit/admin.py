from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in AuditLog._meta.fields]
    list_display = ["action_type", "model_name", "object_id", "user", "ip_address", "created_at"]
    list_filter = ["action_type", "model_name", "created_at"]
    search_fields = ["user__username", "object_id", "ip_address"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
