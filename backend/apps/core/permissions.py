from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()


class IsKitchen(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Kitchen").exists()


class IsDelivery(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Delivery").exists()


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Staff").exists()


class IsITAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="IT_Admin").exists()


class IsManagerOrITAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(
            name__in=["Manager", "IT_Admin"]
        ).exists()
