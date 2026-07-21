import pytest
from apps.audit.models import AuditLog
from apps.audit.services.audit_service import AuditService
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestAuditLogImmutability:

    def test_audit_log_cannot_be_updated(self):
        user = UserFactory()
        log = AuditLog.objects.create(
            user=user,
            action_type="login",
            model_name="User",
            object_id=str(user.pk),
        )
        with pytest.raises(ValueError, match="immutable"):
            log.save()

    def test_audit_log_created_successfully(self):
        user = UserFactory()
        AuditLog.objects.create(
            user=user,
            action_type="login",
            model_name="User",
            object_id=str(user.pk),
        )
        assert AuditLog.objects.filter(user=user, action_type="login").count() == 1


@pytest.mark.django_db
class TestAuditService:

    def test_audit_service_creates_log(self):
        user = UserFactory()
        AuditService.log(user=user, action_type="login", instance=user)
        assert AuditLog.objects.filter(user=user, action_type="login").count() == 1

    def test_audit_service_stores_changes(self):
        user = UserFactory()
        changes = {"old_status": "pending", "new_status": "confirmed"}
        AuditService.log(
            user=user,
            action_type="status_change",
            instance=user,
            changes=changes,
        )
        log = AuditLog.objects.get(user=user, action_type="status_change")
        assert log.changes == changes

    def test_audit_service_works_without_request(self):
        # Pulisce il thread-local per simulare assenza di request
        from apps.audit import middleware as audit_middleware
        audit_middleware._thread_locals.request = None

        user = UserFactory()
        AuditService.log(user=user, action_type="create", instance=user)
        log = AuditLog.objects.get(user=user, action_type="create")
        assert log.ip_address is None
        assert log.user_agent is None
